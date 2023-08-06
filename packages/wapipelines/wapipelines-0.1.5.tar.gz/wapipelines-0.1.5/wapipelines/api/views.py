from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from wapipelines.models import Pipeline, ASYNC_RUNNER
from wapipelines.api.serializers import (
    PipelineSerializer, RunPipelineSerializer)


class PipelineViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PipelineSerializer
    lookup_field = 'uuid'

    def get_queryset(self):
        return Pipeline.objects.filter(user=self.request.user)

    @detail_route(methods=['post'])
    def run(self, request, uuid=None):
        pipeline = self.get_object()
        serializer = RunPipelineSerializer(data=request.data)
        if serializer.is_valid():
            payload = serializer.data['payload']
            inputs = serializer.data.get('inputs', {})
            # NOTE: list for py3 because it returns a dict_keys() type
            if not pipeline.can_run_given(list(inputs.keys())):
                return Response({
                    'inputs': ['No suitable inputs given']
                }, status=status.HTTP_400_BAD_REQUEST)

            run, first_steps = pipeline.run(
                payload,
                inputs=inputs,
                runner=ASYNC_RUNNER)
            return Response({
                'run': run.uuid,
            }, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['post'])
    def direct(self, request, uuid=None):
        pipeline = self.get_object()
        if not pipeline.can_run_given([]):
            return Response({
                'inputs': ['This pipeline requires inputs.']
            }, status=status.HTTP_400_BAD_REQUEST)

        run, first_steps = pipeline.run(
            request.data, inputs=[], runner=ASYNC_RUNNER)
        return Response({
            'run': run.uuid,
        }, status=status.HTTP_202_ACCEPTED)
