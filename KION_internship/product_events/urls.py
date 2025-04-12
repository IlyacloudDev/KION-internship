from django.urls import path
from .views import ProductEventAPIView


urlpatterns = [
    path('', ProductEventAPIView.as_view(), name='send_event_to_rabbitmq')
]
