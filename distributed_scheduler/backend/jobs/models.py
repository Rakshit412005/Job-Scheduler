from django.db import models
from queues.models import Queue


class Job(models.Model):

    STATUS_CHOICES = [
        ('QUEUED', 'QUEUED'),
        ('CLAIMED', 'CLAIMED'),
        ('RUNNING', 'RUNNING'),
        ('COMPLETED', 'COMPLETED'),
        ('FAILED', 'FAILED'),
    ]

    queue = models.ForeignKey(
        Queue,
        on_delete=models.CASCADE,
        related_name='jobs'
    )

    payload = models.JSONField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='QUEUED'
    )

    retry_count = models.IntegerField(default=0)

    is_dead_letter = models.BooleanField(default=False)

    scheduled_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['scheduled_at']),
        ]

    def __str__(self):
        return f"Job {self.id}"


class JobExecution(models.Model):

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='executions'
    )

    worker_name = models.CharField(
        max_length=100
    )

    started_at = models.DateTimeField()

    ended_at = models.DateTimeField(
        null=True,
        blank=True
    )

    success = models.BooleanField(
        default=False
    )

    logs = models.TextField(
        blank=True
    )

    def __str__(self):
        return f"Execution {self.id} - Job {self.job.id}"