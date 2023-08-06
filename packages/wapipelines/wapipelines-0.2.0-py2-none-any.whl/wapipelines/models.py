import logging
import json
import os
import six
import hmac
import hashlib
import binascii
import pkg_resources

from datetime import datetime
from collections import defaultdict

from django.db import models
from django.contrib.postgres import fields
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder

from uuid import uuid4
import requests
import networkx as nx
from networkx.algorithms.dag import topological_sort
from networkx.drawing import nx_pydot

logger = logging.getLogger(__name__)


class PipelineException(Exception):
    pass


class ImpossiblePipelineException(PipelineException):
    pass


class PipelineStepException(PipelineException):
    pass


def run_step_sync(run, step, payload, inputs):
    logger.info('Running %s' % (step.name,))
    pipeline = step.pipeline
    result = step.run_step(run, payload, inputs)
    outputs = step.pipeline.get_outputs(run)
    next_steps = [run_step_sync(run, next_step, payload, outputs)
                  for next_step in step.next_steps(run=run)
                  if next_step.is_ready(outputs)]

    if step.is_exit_point() and pipeline.endpoint:
        pipeline.submit_outputs(run, step)

    return (step, result, next_steps)


def run_step_async(run, step, payload, inputs):
    logger.info('Scheduling %s' % (step.name,))
    from wapipelines.tasks import run_step_task
    return run_step_task.delay(run.pk, step.pk, payload, inputs)


SYNC_RUNNER = run_step_sync
ASYNC_RUNNER = run_step_async


def generate_secret():
    return binascii.hexlify(os.urandom(16))


class Pipeline(models.Model):
    user = models.ForeignKey('auth.User')
    name = models.CharField(max_length=255)
    uuid = models.UUIDField(default=uuid4)
    secret = models.CharField(
        default=generate_secret,
        null=False, blank=True, max_length=255)
    planning = fields.ArrayField(
        models.UUIDField(blank=True, null=True), default=[])
    dot = models.TextField(blank=True, null=True)
    endpoint = models.URLField(blank=True, null=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    EMPTY_INPUTS = {}

    @classmethod
    def graph(cls, pipeline):
        dag = nx.DiGraph()
        steps = pipeline.step_set.all().order_by('created_at')
        for step in steps:
            dag.add_node(step)

        for current_step in steps:
            for next_step in current_step.next_steps():
                dag.add_edge(current_step, next_step)

            for previous_step in current_step.previous_steps():
                dag.add_edge(previous_step, current_step)

        return dag

    @classmethod
    def plan(cls, pipeline):
        try:
            graph = Pipeline.graph(pipeline)
            topological_sort(graph)
            return graph
        except (nx.NetworkXUnfeasible,):
            raise ImpossiblePipelineException()

    @classmethod
    def find_cycles(self, pipeline):
        return nx.simple_cycles(Pipeline.graph(pipeline))

    def hexdigest(self, data, secret=None):
        return hmac.new(
            key=six.b(str(secret or self.secret)),
            msg=six.b(str(data)),
            digestmod=hashlib.sha512).hexdigest()

    def get_default_headers(self, data):
        return {
            'Content-Type': 'application/json',
            'User-Agent': 'WA-Pipeline/%s' % (
                pkg_resources.get_distribution('wapipelines').version),
            'X-WA-Pipeline': self.uuid.hex,
            'X-WA-Sign': self.hexdigest(data),
        }

    def signed_http_post(self, url, data=None, timeout=None,
                         headers={}):
        default_headers = self.get_default_headers(data)
        default_headers.update(headers)
        return requests.post(
            url,
            data=data,
            timeout=timeout,
            headers=default_headers)

    def submit_outputs(self, run, step):
        r = self.signed_http_post(
            self.endpoint,
            data=json.dumps({
                'run': run.serialize(),
                'pipeline': self.serialize(run),
            }, indent=2, cls=DjangoJSONEncoder),
            timeout=(1 * settings.MINUTE),
            headers={
                'X-WA-Step': step.uuid.hex,
                'X-WA-Step-Name': step.name,
            })
        r.raise_for_status()
        return r

    def get_cycles(self):
        return list(Pipeline.find_cycles(self))

    def to_pydot(self):
        return nx_pydot.to_pydot(Pipeline.graph(self))

    def set_plan(self, graph):
        self.dot = nx_pydot.to_pydot(graph).to_string()

    def can_receive(self, other_pipeline):
        connections = []
        for entry_point in self.entry_points():
            for exit_point in other_pipeline.exit_points():
                if entry_point.inputs == exit_point.outputs:
                    connections.append((exit_point, entry_point))
        return connections

    def entry_points(self):
        graph = Pipeline.graph(self)
        return [step for step in graph.nodes()
                if not graph.in_edges(step)]

    def exit_points(self):
        graph = Pipeline.graph(self)
        return [step for step in graph.nodes()
                if not graph.out_edges(step)]

    def can_run_given(self, inputs):
        if not self.active:
            return False
        return inputs in self.allowable_inputs()

    def run(self, payload, inputs=None, runner=None):
        runner = runner or SYNC_RUNNER

        inputs = inputs or self.EMPTY_INPUTS
        run = self.pipelinerun_set.create(
            payload=payload, dot=self.dot,
            expected_outputs=list(self.possible_outputs()))
        steps = self.step_set.filter(
            models.Q(inputs__overlap=list(inputs.keys())) |
            models.Q(inputs__len=0))

        return (run, [runner(run, step, payload, inputs)
                      for step in steps])

    def requires_inputs(self):
        return any([inputs for inputs in self.allowable_inputs()])

    def allowable_inputs(self):
        inputs = []
        # set struggles to make sets of lists of lists
        for step in self.entry_points():
            if step.inputs not in inputs:
                inputs.append(step.inputs)
        return inputs

    def possible_outputs(self):
        return set([
            output
            for step in self.step_set.all()
            for output in step.outputs])

    def get_outputs(self, run):
        result_set = defaultdict(list)
        for result in self.result_set.filter(run=run):
            for key, value in result.outputs.items():
                result_set[key].append(value)
        return dict(result_set)

    def serialize(self, run):
        return {
            'uuid': self.uuid,
            'name': self.name,
            'outputs': self.get_outputs(run)
        }


class Step(models.Model):

    MIN_TIMEOUT = 50
    DEFAULT_TIMEOUT = 100
    ACCEPTABLE_TIMEOUT = 200
    MAX_TIMEOUT = 3000
    GOOGLE_CLOUD_TIMEOUT = 10000

    TIMEOUT_CHOICES = (
        (MIN_TIMEOUT, '50 milliseconds'),
        (DEFAULT_TIMEOUT, '100 milliseconds'),
        (ACCEPTABLE_TIMEOUT, '200 milliseconds'),
        (MAX_TIMEOUT, '3 seconds'),
        (GOOGLE_CLOUD_TIMEOUT, '10 seconds'),
    )

    EMPTY_INPUTS = []
    EMPTY_OUTPUTS = []

    pipeline = models.ForeignKey(Pipeline)
    name = models.CharField(max_length=255, blank=True, null=True)
    uuid = models.UUIDField(default=uuid4)
    inputs = fields.ArrayField(
        models.CharField(max_length=125, blank=True))
    outputs = fields.ArrayField(
        models.CharField(max_length=125, blank=True))
    url = models.URLField(null=True, blank=True)
    headers = fields.JSONField(
        'HTTP headers to submit as part of the step',
        default=dict)
    timeout = models.PositiveIntegerField(
        'Timeout in milliseconds',
        default=DEFAULT_TIMEOUT,
        choices=TIMEOUT_CHOICES)
    error = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_missing_inputs(self, inputs):
        return set(self.inputs) - set(inputs.keys())

    def is_ready(self, inputs):
        return not any(self.get_missing_inputs(inputs))

    def is_noop(self):
        """
        Some steps have no other purpose but to wait for results
        for preceding steps, currently the only way of specifying
        that behaviour is by leaving the URL blank
        """
        return not self.url

    def get_default_headers(self, run):
        return {
            'X-WA-Run': run.uuid.hex,
            'X-WA-Step': self.uuid.hex,
            'X-WA-Step-Name': self.name,
        }

    def run_step(self, run, payload, inputs):
        if self.is_noop():
            return

        start = datetime.now()
        seconds_timeout = (self.timeout / 1000.0)
        response = None
        headers = self.get_default_headers(run)
        headers.update(self.headers)
        try:
            response = self.pipeline.signed_http_post(
                url=self.url,
                data=json.dumps({
                    "payload": payload,
                    "inputs": inputs,
                }, indent=2, cls=DjangoJSONEncoder),
                timeout=seconds_timeout,
                headers=headers
            )
            outputs = response.json()
            response.raise_for_status()
            return self.result_set.create(
                pipeline=self.pipeline,
                run=run,
                inputs=inputs, outputs=outputs,
                duration=datetime.now() - start,
                response_code=response.status_code)
        except (requests.RequestException, ValueError) as e:
            response_code = (response.status_code
                             if response is not None
                             else None)
            return self.result_set.create(
                pipeline=self.pipeline,
                run=run,
                inputs=inputs, outputs={},
                duration=datetime.now() - start,
                response_code=response_code,
                error=str(e))

    def next_steps(self, run=None):
        steps = Step.objects.filter(
            pipeline=self.pipeline, inputs__overlap=self.outputs
        ).order_by('created_at')
        if run is not None:
            steps = steps.exclude(result__run=run)
        return steps

    def previous_steps(self):
        return Step.objects.filter(
            pipeline=self.pipeline, outputs__overlap=self.inputs
        ).order_by('created_at')

    def is_exit_point(self):
        return self in self.pipeline.exit_points()

    def __str__(self):
        return self.name or str(self.uuid)


class PipelineRun(models.Model):
    pipeline = models.ForeignKey(Pipeline)
    uuid = models.UUIDField(default=uuid4)
    dot = models.TextField(null=True, blank=True)
    expected_outputs = fields.ArrayField(
        models.CharField(max_length=255)
    )
    payload = fields.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def still_needs(self, step):
        return not self.result_set.filter(step=step).exists()

    def serialize(self):
        return {
            'uuid': self.uuid,
            'is_completed': self.is_completed(),
            'expected_outputs': self.expected_outputs,
            'created_at': self.created_at,
            'payload': self.payload,
            'errors': [
                result.serialize() for result in self.get_errors()],
            'results': [
                result.serialize() for result in self.result_set.all()]
        }

    def get_errors(self):
        return self.result_set.filter(error__isnull=False)

    def is_completed(self):
        if self.get_errors():
            return False

        return set(self.get_outputs().keys()).issuperset(
            set(self.expected_outputs))

    def get_outputs(self):
        return self.pipeline.get_outputs(self)

    def duration(self):
        aggregate = self.result_set.aggregate(
            duration=(models.Max('created_at') - models.Min('created_at')))
        return aggregate.get('duration')

    def __str__(self):
        return self.uuid.hex


class Result(models.Model):
    pipeline = models.ForeignKey(Pipeline)
    uuid = models.UUIDField(default=uuid4)
    run = models.ForeignKey(PipelineRun)
    step = models.ForeignKey(Step)
    inputs = fields.JSONField(default=dict)
    outputs = fields.JSONField(default=dict)
    duration = models.DurationField()
    response_code = models.PositiveIntegerField(null=True, blank=True)
    error = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def serialize(self):
        return {
            'uuid': self.uuid,
            'created_at': self.created_at,
            'inputs': self.inputs,
            'outputs': self.outputs,
            'step_uuid': self.step.uuid,
            'step_name': self.step.name,
            'duration': self.duration.total_seconds(),
            'error': self.error,
        }

    def get_step_headers(self):
        default_headers = self.pipeline.get_default_headers(
            json.dumps(self.get_step_data(), cls=DjangoJSONEncoder))
        default_headers.update(self.step.get_default_headers(self.run))
        return default_headers

    def get_step_data(self):
        return {
            "payload": self.run.payload,
            "inputs": self.inputs,
        }

    class Meta:
        ordering = ('created_at',)
