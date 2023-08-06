import logging
import json
from django.views.generic.base import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormView

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, reverse
from django.conf import settings
from django.contrib import messages
from random import randint
from time import sleep

from wapipelines.models import Pipeline, Step, ASYNC_RUNNER
from wapipelines.forms import (
    CreatePipelineForm, CreateStepForm, PipelineRunForm)

from digg_paginator import DiggPaginator


logger = logging.getLogger(__name__)


class PipelineListView(ListView):

    model = Pipeline

    def get_queryset(self, *args, **kwargs):
        qs = super(PipelineListView, self).get_queryset(*args, **kwargs)
        return qs.filter(user=self.request.user)


class PipelineCreateView(CreateView):
    model = Pipeline
    form_class = CreatePipelineForm
    ordering = ('created_at',)

    def form_valid(self, form):
        pipeline = form.save(commit=False)
        pipeline.user = self.request.user
        pipeline.save()
        return redirect('pipeline:list')


class PipelineUpdateView(UpdateView):
    model = Pipeline
    form_class = CreatePipelineForm

    def form_valid(self, form):
        pipeline = form.save(commit=False)
        pipeline.user = self.request.user
        pipeline.save()
        return redirect('pipeline:list')


class StepListView(ListView):
    model = Step
    form_class = CreateStepForm
    paginate_by = 10
    paginator_class = DiggPaginator
    ordering = ('-created_at',)

    def get_context_data(self, *args, **kwargs):
        pipeline = get_object_or_404(
            Pipeline, user=self.request.user,
            pk=self.kwargs['pipeline_pk'])
        context = super(StepListView, self).get_context_data(*args, **kwargs)
        context.update({
            'pipeline': pipeline,
            'runs': pipeline.pipelinerun_set.order_by('-created_at')[:100],
            'form': self.form_class(initial={
                'pipeline': pipeline,
            }),
            'run_form': PipelineRunForm(),
        })
        return context

    def get_queryset(self, *args, **kwargs):
        return Step.objects.filter(
            pipeline__pk=self.kwargs['pipeline_pk'],
            pipeline__user=self.request.user).order_by('created_at')


class StepCreateView(CreateView):
    model = Step
    form_class = CreateStepForm

    def form_valid(self, form):
        step = form.save(commit=False)
        step.pipeline = get_object_or_404(
            Pipeline,
            user=self.request.user,
            pk=self.kwargs['pipeline_pk'])
        step.save()
        return redirect(
            'pipeline:step_list', pipeline_pk=step.pipeline.pk)


class StepUpdateView(UpdateView):
    model = Step
    form_class = CreateStepForm

    def form_valid(self, form):
        step = form.save(commit=False)
        step.pipeline = get_object_or_404(
            Pipeline,
            user=self.request.user,
            pk=self.kwargs['pipeline_pk'])
        step.save()
        return redirect(
            'pipeline:step_list', pipeline_pk=step.pipeline.pk)


class StepDeleteView(DeleteView):
    model = Step

    def get_queryset(self, *args, **kwargs):
        pipeline = get_object_or_404(
            self.request.user.pipeline_set, pk=self.kwargs['pipeline_pk'])
        return pipeline.step_set.all()

    def get_success_url(self):
        pipeline = get_object_or_404(
            self.request.user.pipeline_set, pk=self.kwargs['pipeline_pk'])
        return reverse('pipeline:step_list', kwargs={
            'pipeline_pk': pipeline.pk,
        })


class PipelineRunView(FormView):
    template_name = 'wapipelines/pipeline_run.html'
    form_class = PipelineRunForm

    def form_valid(self, form):
        pipeline = get_object_or_404(
            self.request.user.pipeline_set.all(), pk=self.kwargs['pk'])
        data = form.cleaned_data['data']
        pipeline.run(data, runner=ASYNC_RUNNER)
        messages.info(self.request, 'Pipeline run started')
        return redirect(
            'pipeline:step_list', pipeline_pk=pipeline.pk)


class ArtefactView(View):

    def get(self, request, artefact):
        return JsonResponse({
            "inputs": request.GET.getlist('inputs'),
            "outputs": [artefact],
        }, json_dumps_params={
            'indent': 2,
        })

    def post(self, request, artefact):
        logger.info('Received payload: %s' % (json.load(request),))
        naptime = randint(1, 2) if settings.DEBUG else 0
        logger.info('napping %s for %s seconds' % (artefact, naptime,))
        sleep(naptime)
        return JsonResponse({
            artefact: 'value of %s' % (artefact,),
        })
