import os
import sys
import time
import django

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "backend.settings"
)

django.setup()

from django.db import transaction
from django.utils import timezone

from jobs.models import Job, JobExecution
from workers.models import Worker


worker, created = Worker.objects.get_or_create(
    name="worker-1"
)

worker.status = "ACTIVE"
worker.save()


def update_heartbeat():
    worker.heartbeat = timezone.now()
    worker.status = "ACTIVE"
    worker.save()


def claim_job():

    with transaction.atomic():

        job = (
            Job.objects
            .select_for_update(skip_locked=True)
            .filter(status='QUEUED')
            .first()
        )

        if job:
            job.status = "CLAIMED"
            job.save()

        return job


def execute_job(job):

    execution = JobExecution.objects.create(
        job=job,
        worker_name=worker.name,
        started_at=timezone.now(),
        success=False,
        logs=""
    )

    try:

        print(f"\nExecuting Job {job.id}")

        job.status = "RUNNING"
        job.save()

        if job.id % 2 == 0:
            raise Exception(
                "Simulated failure"
            )

        time.sleep(5)

        job.status = "COMPLETED"
        job.save()

        execution.success = True
        execution.logs = "Job completed"
        execution.ended_at = timezone.now()
        execution.save()

        print(
            f"Completed Job {job.id}"
        )

    except Exception as e:

        print(
            f"Failed Job {job.id}"
        )

        execution.success = False
        execution.logs = str(e)
        execution.ended_at = timezone.now()
        execution.save()

        job.retry_count += 1

        if job.retry_count <= 3:

            print(
                f"Retrying Job {job.id}"
            )

            job.status = "QUEUED"

        else:

            print(
                f"Moving Job {job.id} to DLQ"
            )

            job.status = "FAILED"
            job.is_dead_letter = True

        job.save()


def worker_loop():

    print("\nWorker started")

    while True:

        update_heartbeat()

        job = claim_job()

        if job:
            execute_job(job)
        else:
            print(
                "No jobs available"
            )

        time.sleep(2)


if __name__ == "__main__":

    try:
        worker_loop()

    except KeyboardInterrupt:

        worker.status = "IDLE"
        worker.save()

        print(
            "\nWorker shutting down gracefully"
        )

    except Exception as e:

        worker.status = "DOWN"
        worker.save()

        print(
            f"\nWorker crashed: {e}"
        )