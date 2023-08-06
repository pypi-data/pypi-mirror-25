from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from wapipelines import views

urlpatterns = [
    url(r'^$',
        login_required(views.PipelineListView.as_view()),
        name='list'),
    url(r'^create/$',
        login_required(views.PipelineCreateView.as_view()),
        name='create'),
    url(r'^(?P<pk>\d+)/update/$',
        login_required(views.PipelineUpdateView.as_view()),
        name='update'),
    url(r'^(?P<pk>\d+)/run/$',
        login_required(views.PipelineRunView.as_view()),
        name='run'),
    url(r'^(?P<pipeline_pk>\d+)/$',
        login_required(views.StepListView.as_view()),
        name='step_list'),
    url(r'^(?P<pipeline_pk>\d+)/create/$',
        login_required(views.StepCreateView.as_view()),
        name='step_create'),
    url(r'^(?P<pipeline_pk>\d+)/steps/(?P<pk>\d+)/$',
        login_required(views.StepUpdateView.as_view()),
        name='step_update'),
    url(r'^(?P<pipeline_pk>\d+)/steps/(?P<pk>\d+)/delete/$',
        login_required(views.StepDeleteView.as_view()),
        name='step_delete'),
]
