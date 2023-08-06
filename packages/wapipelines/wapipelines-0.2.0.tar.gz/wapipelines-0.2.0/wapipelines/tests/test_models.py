import json
import responses
import hmac
import hashlib
import six
from uuid import UUID

from django.contrib.auth.models import User
from django.test import TestCase

from wapipelines.models import (
    Pipeline,
    ImpossiblePipelineException,
    Step)


ARTEFACT_1 = 'artefact-1'
ARTEFACT_2 = 'artefact-2'
ARTEFACT_3 = 'artefact-3'
ARTEFACT_4 = 'artefact-4'


class PipelineTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            'username', 'test@example.org', 'password')
        self.pipeline = Pipeline.objects.create(
            user=self.user,
            name='test pipeline')

    def mk_simple_steps(self, pipeline,
                        url='http://example.org/',
                        timeout=Step.ACCEPTABLE_TIMEOUT):
        step1 = pipeline.step_set.create(
            url=url,
            name="step1",
            timeout=timeout,
            inputs=Step.EMPTY_INPUTS,
            outputs=[ARTEFACT_1])
        step2_1 = pipeline.step_set.create(
            url=url,
            name="step2_1",
            timeout=timeout,
            inputs=step1.outputs,
            outputs=[ARTEFACT_2])
        step2_2 = pipeline.step_set.create(
            url=url,
            name="step2_2",
            timeout=timeout,
            inputs=step1.outputs,
            outputs=[ARTEFACT_3])
        step3 = pipeline.step_set.create(
            url=url,
            name="step3",
            timeout=timeout,
            inputs=step2_1.outputs + step2_2.outputs,
            outputs=[ARTEFACT_4])
        step4 = pipeline.step_set.create(
            url=url,
            name="step4",
            timeout=timeout,
            inputs=step3.outputs,
            outputs=Step.EMPTY_OUTPUTS)
        return (step1, step2_1, step2_2, step3, step4)

    def mk_impossible_steps(self, pipeline, url='http://example.org/'):
        step1 = pipeline.step_set.create(
            url=url,
            inputs=[ARTEFACT_1],
            outputs=[ARTEFACT_2])
        step2 = pipeline.step_set.create(
            url=url,
            inputs=[ARTEFACT_2],
            outputs=[ARTEFACT_1])
        return (step1, step2)

    def test_planning(self):
        steps = self.mk_simple_steps(self.pipeline)
        step1, step2_1, step2_2, step3, step4 = steps
        graph = Pipeline.plan(self.pipeline)
        self.assertEqual(
            set(graph.nodes()),
            set(steps))

    def test_detect_impossible_plan(self):
        step1, step2 = self.mk_impossible_steps(self.pipeline)
        self.assertRaises(
            ImpossiblePipelineException,
            Pipeline.plan, self.pipeline)

    def test_find_cycles(self):
        step1, step2 = self.mk_impossible_steps(self.pipeline)
        [cycle] = self.pipeline.get_cycles()
        self.assertEqual(
            set(cycle),
            set([step1, step2]))

    def test_save_planning(self):
        self.mk_simple_steps(self.pipeline)
        graph = Pipeline.plan(self.pipeline)
        self.pipeline.set_plan(graph)
        self.pipeline.save()

        reloaded = Pipeline.objects.get(pk=self.pipeline.pk)
        self.assertEqual(
            reloaded.dot,
            self.pipeline.to_pydot().to_string())

    @responses.activate
    def test_run(self):
        payload = {
            ARTEFACT_1: "value for artefact-1",
            ARTEFACT_2: "value for artefact-2",
            ARTEFACT_3: "value for artefact-3",
            ARTEFACT_4: "value for artefact-4",
        }
        responses.add(
            responses.POST, 'http://example.org/',
            content_type='application/json',
            json=payload)

        steps = self.mk_simple_steps(self.pipeline)
        plan = Pipeline.plan(self.pipeline)
        self.pipeline.set_plan(plan)

        self.pipeline.run({})

        results = self.pipeline.result_set.all()
        # We should run each step only once for each pipeline run
        self.assertEqual(results.count(), len(steps))
        for index, result in enumerate(results):
            self.assertEqual(result.step.pipeline, self.pipeline)
            if index == 0:
                self.assertEqual(result.inputs, {})
            else:
                self.assertEqual(
                    result.inputs.keys(), payload.keys())

            self.assertEqual(result.outputs, payload)
            self.assertEqual(result.response_code, 200)
            self.assertTrue(result.duration.total_seconds())

    @responses.activate
    def test_run_in_parallel(self):

        responses.add(
            responses.POST, 'http://example.org/step1/',
            content_type='application/json',
            json={
                ARTEFACT_1: 'value-for-step-1'
            })
        responses.add(
            responses.POST, 'http://example.org/step2/',
            content_type='application/json',
            json={
                ARTEFACT_2: 'value-for-step-2'
            })
        responses.add(
            responses.POST, 'http://example.org/step3/',
            content_type='application/json',
            json={
                ARTEFACT_3: 'value-for-step-3'
            })
        responses.add(
            responses.POST, 'http://example.org/step4/',
            content_type='application/json',
            json={
                ARTEFACT_4: 'value-for-step-4'
            })

        self.pipeline.step_set.create(
            url='http://example.org/step1/',
            name="step1",
            timeout=Step.ACCEPTABLE_TIMEOUT,
            inputs=Step.EMPTY_INPUTS,
            outputs=[ARTEFACT_1])
        self.pipeline.step_set.create(
            url='http://example.org/step2/',
            name="step2",
            timeout=Step.ACCEPTABLE_TIMEOUT,
            inputs=[ARTEFACT_1],
            outputs=[ARTEFACT_2])
        self.pipeline.step_set.create(
            url='http://example.org/step3/',
            name="step3",
            timeout=Step.ACCEPTABLE_TIMEOUT,
            inputs=[ARTEFACT_1],
            outputs=[ARTEFACT_3])
        self.pipeline.step_set.create(
            url='http://example.org/step4/',
            name="step4",
            timeout=Step.ACCEPTABLE_TIMEOUT,
            inputs=[ARTEFACT_2, ARTEFACT_3],
            outputs=[ARTEFACT_4])

        self.pipeline.run({})

        [run] = self.pipeline.pipelinerun_set.all()
        results = self.pipeline.result_set.all()
        self.assertEqual(
            results.count(),
            4)
        outputs = self.pipeline.get_outputs(run)
        self.assertEqual(outputs, {
            ARTEFACT_1: ['value-for-step-1'],
            ARTEFACT_2: ['value-for-step-2'],
            ARTEFACT_3: ['value-for-step-3'],
            ARTEFACT_4: ['value-for-step-4'],
        })

    @responses.activate
    def test_log_error(self):

        def explode(request):
            return (503, {}, '{}')

        responses.add_callback(
            responses.POST, 'http://example.org/step1/',
            callback=explode,
            content_type='application/json')

        self.pipeline.step_set.create(
            url='http://example.org/step1/',
            name="step1",
            timeout=Step.ACCEPTABLE_TIMEOUT,
            inputs=Step.EMPTY_INPUTS,
            outputs=[ARTEFACT_1])

        self.pipeline.run({})

        [run] = self.pipeline.pipelinerun_set.all()
        [result] = self.pipeline.result_set.all()
        self.assertTrue('503 Server Error' in result.error)
        self.assertEqual(result.response_code, 503)

    @responses.activate
    def test_signing(self):

        def explode(request):
            signing = hmac.new(
                key=six.b(str(self.pipeline.secret)),
                msg=six.b(str(request.body)),
                digestmod=hashlib.sha512)

            self.assertEqual(
                request.headers['X-WA-Sign'],
                signing.hexdigest())

            return (202, {}, '{}')

        responses.add_callback(
            responses.POST, 'http://example.org/step1/',
            callback=explode,
            content_type='application/json')

        self.pipeline.step_set.create(
            url='http://example.org/step1/',
            name="step1",
            timeout=Step.ACCEPTABLE_TIMEOUT,
            inputs=Step.EMPTY_INPUTS,
            outputs=[ARTEFACT_1])

        self.pipeline.run({})
        self.assertEqual(len(responses.calls), 1)

    def test_entry_points(self):
        step1, step2_1, step_2_2, step3, step4 = self.mk_simple_steps(
            self.pipeline)

        [entrypoint] = self.pipeline.entry_points()
        self.assertEqual(entrypoint, step1)

    def test_exit_points(self):
        step1, step2_1, step_2_2, step3, step4 = self.mk_simple_steps(
            self.pipeline)

        [exitpoint] = self.pipeline.exit_points()
        self.assertEqual(exitpoint, step4)

    def test_connect_pipelines(self):
        pipeline1 = Pipeline.objects.create(
            user=self.user,
            name='pipeline1')
        step1_1 = pipeline1.step_set.create(
            url='http://www.example.org',
            name='step 1 for pipeline 1',
            inputs=Step.EMPTY_INPUTS,
            outputs=[ARTEFACT_1])
        step1_2 = pipeline1.step_set.create(
            url='http://www.example.org',
            name='step 2 for pipeline 1',
            inputs=[ARTEFACT_1],
            outputs=[ARTEFACT_2])

        pipeline2 = Pipeline.objects.create(
            user=self.user,
            name='pipeline2')
        step2_1 = pipeline2.step_set.create(
            url='http://www.example.org',
            name='step 1 for pipeline 2',
            inputs=[ARTEFACT_2],
            outputs=[ARTEFACT_3])
        step2_2 = pipeline2.step_set.create(
            url='http://www.example.org',
            name='step 2 for pipeline 2',
            inputs=[ARTEFACT_3],
            outputs=[ARTEFACT_4])

        self.assertEqual(pipeline1.entry_points(), [step1_1])
        self.assertEqual(pipeline1.exit_points(), [step1_2])
        self.assertEqual(pipeline2.entry_points(), [step2_1])
        self.assertEqual(pipeline2.exit_points(), [step2_2])

        self.assertEqual(
            pipeline2.can_receive(pipeline1),
            [(step1_2, step2_1)])
        self.assertEqual(
            pipeline1.can_receive(pipeline2),
            [])

    @responses.activate
    def test_submit_outputs(self):

        responses.add(
            responses.POST, 'http://example.org/step/',
            content_type='application/json',
            json={"foo": "bar"})

        def cb(request):
            data = json.loads(request.body)
            self.assertEqual(data["pipeline"]["outputs"], {
                "foo": ["bar"]
            })
            self.assertEqual(
                UUID(data["pipeline"]["uuid"]),
                self.pipeline.uuid)
            return (202, {}, "{}")

        responses.add_callback(
            responses.POST, 'http://example.org/endpoint/',
            content_type='application/json', callback=cb)

        self.pipeline.step_set.create(
            url='http://example.org/step/',
            name='step1',
            inputs=Step.EMPTY_INPUTS,
            outputs=Step.EMPTY_OUTPUTS)
        self.pipeline.endpoint = 'http://example.org/endpoint/'
        self.pipeline.run({})
        self.assertEqual(len(responses.calls), 2)
