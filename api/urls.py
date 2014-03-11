from django.conf.urls import patterns, url
from browser import views

urlpatterns = patterns('',
    url(r'^topics/$', views.TopicList.as_view()),
    url(r'^documents/$', views.DocumentList.as_view()),
)