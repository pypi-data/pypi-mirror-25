from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from rest import views

urlpatterns = [
    url(r'^events/$', views.on_event),
    url(r'^celery1/$', views.invoke_celery_1),
]

urlpatterns = format_suffix_patterns(urlpatterns)