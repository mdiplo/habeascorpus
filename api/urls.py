from django.conf.urls import patterns, url, include
from api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'topics', views.TopicViewSet)
router.register(r'documents', views.DocumentViewSet)

urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^topics/(?P<pk>[0-9]+)/related_documents$', views.TopicRelatedDocuments.as_view()),
)