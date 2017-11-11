from django.conf.urls import url

from simserver import views

urlpatterns = [
    url(r'^', view = views.diploisation, name='diploisation'),
]
