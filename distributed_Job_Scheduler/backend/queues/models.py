# Create your models here.
from django.db import models
from projects.models import Project


class Queue(models.Model):

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='queues'
    )

    name = models.CharField(max_length=100)

    priority = models.IntegerField(default=1)

    concurrency_limit = models.IntegerField(default=5)

    max_retries = models.IntegerField(default=3)

    paused = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name