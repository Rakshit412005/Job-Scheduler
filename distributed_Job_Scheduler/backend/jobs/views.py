from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Job
from .serializers import JobSerializer


class JobListCreateView(generics.ListCreateAPIView):

    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Job.objects.filter(
            queue__project__owner=self.request.user
        )