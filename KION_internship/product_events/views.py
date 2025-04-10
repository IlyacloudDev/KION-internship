from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductEventSerializer
from .tasks import send_to_rabbitmq


class ProductEventAPIView(APIView):
    """
    API endpoint for receiving product events and queuing them to RabbitMQ.
    """
    def post(self, request):
        """
        Validate incoming product event and send it to RabbitMQ asynchronously.
        """
        serializer = ProductEventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        send_to_rabbitmq.delay(request.data)
        return Response({"status": "queued"}, status=status.HTTP_202_ACCEPTED)
