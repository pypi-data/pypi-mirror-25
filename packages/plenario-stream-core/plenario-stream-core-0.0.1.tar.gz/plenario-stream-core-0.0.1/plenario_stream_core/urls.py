from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^submit/', views.accept_payload, name='payload'),
    url(r'^status/', views.accept_job_status, name='status'),
]
