# Distributed Job Scheduler

A distributed job scheduling and execution system built using **Django**, **Django REST Framework**, and a custom **Python Worker Service**. The system supports job scheduling, distributed execution, retry policies, dead letter queues, execution logging, worker heartbeats, and atomic job claiming.

---

# Project Overview

The Distributed Job Scheduler is designed to efficiently manage and execute asynchronous tasks using a queue-based architecture.

The system provides:

- User authentication using JWT
- Project-based queue management
- Distributed worker execution
- Retry mechanisms
- Dead Letter Queue (DLQ)
- Execution logging
- Worker heartbeat monitoring
- Atomic job claiming
- Concurrent-safe processing

---

# Features

## Authentication
- User registration
- JWT-based login
- Protected APIs

## Project Management
- Create projects
- View projects

## Queue Management
- Create queues
- Configure priorities
- Configure concurrency limits
- Configure retry policies

## Job Management
- Submit jobs
- Monitor job status
- Retry failed jobs
- Schedule future jobs

## Worker Service
- Poll jobs continuously
- Atomic job claiming
- Execute jobs
- Retry failed jobs
- Dead Letter Queue handling
- Execution logging
- Heartbeat monitoring

## Reliability Features
- Retry policies
- Dead Letter Queue
- Worker heartbeats
- Transaction-safe execution
- Graceful shutdown
- Execution history tracking

---

#  Technology Stack

| Component | Technology |
|-----------|------------|
| Backend | Django 5 |
| API Framework | Django REST Framework |
| Authentication | JWT |
| Database | SQLite / PostgreSQL |
| Worker Service | Python |
| ORM | Django ORM |

---

# System Architecture

```
                 Client / Frontend
                          |
                          | JWT Authentication
                          v
                 +------------------+
                 | Django REST API  |
                 +------------------+
                    |      |      |
                    v      v      v
               Projects Queues Jobs
                          |
                          v
               +--------------------+
               | Database           |
               | SQLite/PostgreSQL  |
               +--------------------+
                          ^
                          |
                          |
               +--------------------+
               | Worker Service     |
               +--------------------+
               | Poll Jobs          |
               | Atomic Claiming    |
               | Status Updates     |
               | Execution Logs     |
               | Worker Heartbeats  |
               +--------------------+
                          |
                          v
                    Retry Engine
                          |
                          v
                  Dead Letter Queue
```

---

# Database Schema

## USER

| Field | Type |
|-------|------|
| id | int |
| username | string |
| email | string |
| password | string |

---

## PROJECT

| Field | Type |
|-------|------|
| id | int |
| owner_id | FK |
| name | string |
| description | string |
| created_at | datetime |

---

## QUEUE

| Field | Type |
|-------|------|
| id | int |
| project_id | FK |
| name | string |
| priority | int |
| concurrency_limit | int |
| max_retries | int |
| paused | boolean |
| created_at | datetime |

---

## JOB

| Field | Type |
|-------|------|
| id | int |
| queue_id | FK |
| payload | JSON |
| status | string |
| retry_count | int |
| is_dead_letter | boolean |
| scheduled_at | datetime |
| created_at | datetime |
| updated_at | datetime |

---

## JOB_EXECUTION

| Field | Type |
|-------|------|
| id | int |
| job_id | FK |
| worker_name | string |
| started_at | datetime |
| ended_at | datetime |
| success | boolean |
| logs | text |

---

## WORKER

| Field | Type |
|-------|------|
| id | int |
| name | string |
| status | string |
| heartbeat | datetime |

---

# 🔄 Job Lifecycle

## Successful Execution

```
QUEUED
   ↓
CLAIMED
   ↓
RUNNING
   ↓
COMPLETED
```

---

## Failure Flow

```
RUNNING
   ↓
FAILED
   ↓
RETRY
   ↓
FAILED
   ↓
RETRY
   ↓
FAILED
   ↓
DEAD LETTER QUEUE
```

---

# API Endpoints

## Authentication

### Register User

```http
POST /api/register/
```

Example:

```json
{
    "username": "admin",
    "email": "admin@gmail.com",
    "password": "admin123"
}
```

---

### Login User

```http
POST /api/login/
```

Example:

```json
{
    "username": "admin",
    "password": "admin123"
}
```

Returns:

```json
{
    "refresh": "...",
    "access": "..."
}
```

---

## Project APIs

### Create Project

```http
POST /api/projects/
```

Example:

```json
{
    "name": "Distributed Scheduler",
    "description": "Intern Assignment"
}
```

---

### List Projects

```http
GET /api/projects/
```

---

## Queue APIs

### Create Queue

```http
POST /api/queues/
```

Example:

```json
{
    "project": 1,
    "name": "high-priority",
    "priority": 10,
    "concurrency_limit": 5,
    "max_retries": 3
}
```

---

### List Queues

```http
GET /api/queues/
```

---

## Job APIs

### Create Job

```http
POST /api/jobs/
```

Example:

```json
{
    "queue": 1,
    "payload": {
        "task": "send_email",
        "user": "alice"
    }
}
```

---

### List Jobs

```http
GET /api/jobs/
```

---

# Worker Service

The worker service performs:

- Polling queued jobs
- Atomic job claiming
- Executing jobs
- Updating job status
- Logging executions
- Updating worker heartbeats
- Retrying failed jobs
- Moving failed jobs to DLQ

---

# Atomic Job Claiming

To prevent multiple workers from processing the same job, row-level locking is used:

```python
Job.objects.select_for_update(skip_locked=True)
```

This ensures:

- Concurrent-safe processing
- Transactional execution
- Distributed worker support

---

# Retry Mechanism

Failed jobs are retried automatically.

Example:

```
Job 4
Failed
Retry 1

Job 4
Failed
Retry 2

Job 4
Failed
Retry 3

Job 4
Moved to Dead Letter Queue
```

---

# Dead Letter Queue

Jobs exceeding maximum retry limits are marked as:

```python
is_dead_letter = True
```

These jobs are excluded from future processing.

---

# Execution Logging

Every execution attempt is recorded in:

```
JobExecution
```

Captured data:

- Worker Name
- Start Time
- End Time
- Success Status
- Error Logs

---

# Worker Heartbeats

Workers periodically update their heartbeat:

```python
worker.heartbeat = timezone.now()
```

This enables worker health monitoring.

---

#  Graceful Shutdown

The worker supports graceful shutdown:

```python
try:
    worker_loop()
except KeyboardInterrupt:
    worker.status = "IDLE"
```

---

# Project Structure

```
distributed_scheduler/
│
├── backend/
│   ├── accounts/
│   ├── projects/
│   ├── queues/
│   ├── jobs/
│   ├── workers/
│   ├── backend/
│   ├── manage.py
│
├── diagrams/
│   ├── er_diagram.png
│   ├── architecture_diagram.png
│
├── screenshots/
│
├── requirements.txt
│
└── README.md
```

---

# Installation

## Clone Repository

```bash
git clone <repository-url>
cd distributed_scheduler
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Create Superuser

```bash
python manage.py createsuperuser
```

---

## Start Django Server

```bash
python manage.py runserver
```

---

## Start Worker Service

```bash
python workers/worker.py
```

---

#  Screenshots

Include screenshots for:

- Login API
![alt text](image.png)
- Project Creation API

- Queue Creation API
![alt text](image-1.png)
- Job Creation API
![alt text](<Screenshot 2026-07-03 021501.png>)
- Worker Execution
![alt text](image-2.png)
- Retry Mechanism
![alt text](image-3.png)
- Dead Letter Queue
![alt text](image-4.png)
- Django Admin Panel
![alt text](image-5.png)
- ER Diagram
![alt text](<User-Centric Project Job-2026-07-02-200828.png>)
- Architecture Diagram
![alt text](architecture.png)

---

#  Future Enhancements

- Multiple distributed workers
- Redis-based message broker
- Celery integration
- Priority scheduling algorithms
- Kubernetes deployment
- Monitoring dashboard
- Prometheus integration
- Grafana dashboards

---

#  Project Outcome

The Distributed Job Scheduler successfully demonstrates:

- Distributed task execution
- Concurrent-safe processing
- Atomic job claiming
- Retry mechanisms
- Dead Letter Queues
- Worker monitoring
- Execution logging
- Transactional reliability
- Scalable queue architecture

---

# How to Run

## 1. Clone the Repository
```bash
git clone https://github.com/Rakshit412005/Job-Scheduler.git
cd Job-Scheduler
````

## 2. Create a Virtual Environment

```bash
python -m venv venv
```

### Activate the Virtual Environment

**Windows**

```bash
venv\Scripts\activate
```

**Linux/macOS**

```bash
source venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Navigate to the Backend Directory

```bash
cd distributed_scheduler/backend
```

## 5. Apply Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## 6. Create an Admin User

```bash
python manage.py createsuperuser
```

Provide:

* Username
* Email
* Password

## 7. Start the Django Server

```bash
python manage.py runserver
```

The application will be available at:

* [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
* Django Admin: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

## 8. Start the Worker Service

Open a new terminal window and run:

```bash
cd distributed_scheduler/backend/workers
python worker.py
```

The worker will start polling for jobs.

## 9. Test the APIs

Authenticate and obtain a JWT token:

```http
POST http://127.0.0.1:8000/api/login/
```

Use the access token to:

* Create projects
* Create queues
* Submit jobs
* Monitor job execution

## 10. Monitor Execution

Open Django Admin:

* [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

Monitor:

* Projects
* Queues
* Jobs
* Job Executions
* Workers
* Dead Letter Queue Entries

```

