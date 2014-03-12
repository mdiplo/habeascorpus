from django.conf.urls import patterns, url, include
from api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'topics', views.TopicViewSet)
router.register(r'documents', views.DocumentViewSet)

urlpatterns = patterns('',
    url(r'^', include(router.urls)),
)