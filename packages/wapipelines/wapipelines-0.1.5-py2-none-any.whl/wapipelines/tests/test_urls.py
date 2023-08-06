
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings

from rest_framework import routers

from wapipelines.api import views

router = routers.SimpleRouter()
router.register(r'pipeline', views.PipelineViewSet, 'pipeline')


urlpatterns = [
    url(r'^', include('wapipelines.urls', namespace='pipeline')),
    url(r'^api/', include(router.urls, namespace='api')),
    url(r'^admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
