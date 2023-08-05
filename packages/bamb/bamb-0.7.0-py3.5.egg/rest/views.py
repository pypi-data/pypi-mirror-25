from rest_framework import status
from rest_framework.decorators import api_view
import web.wsgi
import rest
import django.http


@api_view(['POST'])
def on_event(request, format=None):

    if request.method == 'POST':
        e = request.data
        print("received : ", e)
        a = web.wsgi.application
        b = rest.apps.RestConfig

        return django.http.HttpResponse(None, status=status.HTTP_201_CREATED)


def invoke_celery_1(request):
    pass