from django.conf.urls import include, url

urlpatterns = [
    url(r'^simserver/', include('simserver.urls')),
]
