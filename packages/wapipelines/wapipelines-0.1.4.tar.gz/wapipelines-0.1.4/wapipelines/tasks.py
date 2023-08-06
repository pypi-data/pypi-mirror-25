from celery import shared_task
from celery.utils.log import get_task_logger

from requests import HTTPError


logger = get_task_logger(__name__)


@shared_task(autoretry_for=(HTTPError,),
             retry_kwargs={'max_retries': 5})
def run_step_task(run_pk, step_pk, payload, inputs):
    from wapipelines.models import Step, PipelineRun
    step = Step.objects.get(pk=step_pk)
    pipeline = step.pipeline
    run = PipelineRun.objects.get(pk=run_pk)
    logger.info('Running step %s for %s with inputs %s' % (
        step.name, run.uuid, inputs.keys()))

    # NOTE: Because of transaction management, this may return
    #       True for two tasks running at the same time
    #       resulting in tasks doing the same things twice.
    #
    #       For now that is OK.
    if run.still_needs(step):
        step.run_step(run, payload, inputs)
    outputs = step.pipeline.get_outputs(run)
    [run_step_task.delay(run.pk, next_step.pk, payload, outputs)
     for next_step in step.next_steps(run=run)
     if next_step.is_ready(outputs)]

    if step.is_exit_point() and pipeline.endpoint:
        pipeline_submit_outputs.delay(run.pk, step.pk)


@shared_task(autoretry_for=(HTTPError,),
             retry_kwargs={'max_retries': 5})
def pipeline_submit_outputs(run_pk, step_pk):
    from wapipelines.models import Step, PipelineRun
    step = Step.objects.get(pk=step_pk)
    pipeline = step.pipeline
    run = PipelineRun.objects.get(pk=run_pk)
    pipeline.submit_outputs(run, step)
