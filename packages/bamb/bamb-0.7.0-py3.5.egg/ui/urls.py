from django.conf.urls import url
from ui import views

urlpatterns = [
    url(r'^ui/websocket/', views.simple_websocket_client),
]