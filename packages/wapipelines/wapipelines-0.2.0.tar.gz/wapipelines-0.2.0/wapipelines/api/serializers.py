from rest_framework import serializers
from wapipelines.models import Pipeline


class PipelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pipeline
        fields = ('uuid', 'name', 'endpoint')


class RunPipelineSerializer(serializers.Serializer):
    payload = serializers.JSONField()
    inputs = serializers.DictField()
