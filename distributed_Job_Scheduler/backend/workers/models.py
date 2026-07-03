from django.db import models
from django.utils import timezone


class Worker(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    status = models.CharField(
        max_length=20,
        default='IDLE'
    )

    heartbeat = models.DateTimeField(
        default=timezone.now
    )

    def __str__(self):
        return self.name