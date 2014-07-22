from django.conf.urls import patterns, url

from simserver import views

urlpatterns = patterns('',
    url(r'^$', views.diploisation, name='diploisation'),
)
