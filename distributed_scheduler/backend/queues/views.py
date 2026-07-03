from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Queue
from .serializers import QueueSerializer


class QueueListCreateView(generics.ListCreateAPIView):

    serializer_class = QueueSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Queue.objects.filter(
            project__owner=self.request.user
        )