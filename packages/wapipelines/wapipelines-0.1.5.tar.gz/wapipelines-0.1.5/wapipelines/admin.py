from django.contrib import admin
from wapipelines.models import Pipeline, Step, Result


admin.site.register(Pipeline)
admin.site.register(Step)
admin.site.register(Result)
