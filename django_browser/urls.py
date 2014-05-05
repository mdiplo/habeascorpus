from django.conf.urls import url

from django_browser import views

urlpatterns = [
    url(r'^$', views.index, name='index')
]
