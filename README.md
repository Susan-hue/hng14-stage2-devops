# Stage 2 DevOps — Containerized Job Processing System

A multi-service job processing system containerized with Docker and deployed
via a full CI/CD pipeline using GitHub Actions.

## Services

- **Frontend** — Node.js/Express server where users submit and track jobs
- **API** — Python/FastAPI service that creates jobs and serves status updates
- **Worker** — Python service that picks up and processes jobs from the queue
- **Redis** — Shared message queue between the API and worker

---

## Prerequisites

Make sure the following are installed on your machine:

- [Docker](https://docs.docker.com/get-docker/) (v20+)
- [Docker Compose](https://docs.docker.com/compose/install/) (v1.29+)
- [Git](https://git-scm.com/)

---

## Quickstart — Bring the Stack Up on a Clean Machine

### 1. Clone the repository

```bash
git clone https://github.com/Susan-hue/hng14-stage2-devops
cd hng14-stage2-devops
```

### 2. Create your environment file

```bash
cp .env.example .env
```

Open `.env` and fill in real values:

```bash
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=your_strong_password_here
API_HOST=0.0.0.0
API_PORT=8000
API_URL=http://api:8000
PORT=3000
```

### 3. Build and start all services

```bash
docker-compose up --build -d
```

### 4. Verify all services are running

```bash
docker-compose ps
```

Expected output:
 Name               Command               State                Ports

app_api_1        uvicorn main:app ...          Up (healthy)     8000/tcp
app_frontend_1   node app.js                   Up (healthy)     0.0.0.0:3000->3000/tcp
app_redis_1      docker-entrypoint.sh ...      Up (healthy)     6379/tcp
app_worker_1     python worker.py              Up (healthy)

All four services should show `Up (healthy)` before proceeding.

### 5. Access the application

Open your browser and visit:
http://localhost:3000

---

## Verifying Each Service

### Frontend
```bash
curl http://localhost:3000/health
```

### API
```bash
curl http://localhost:8000/health
```
Expected response: `{"status": "ok"}`

### Submit a job manually
```bash
curl -X POST http://localhost:3000/submit
```
Expected response: `{"job_id": "<uuid>"}`

### Check job status
```bash
curl http://localhost:3000/status/<job_id>
```
Expected response: `{"job_id": "<uuid>", "status": "completed"}`

---

## CI/CD Pipeline

The pipeline runs automatically on every push to `main` via GitHub Actions
and executes the following stages in strict order:
lint → test → build → security scan → integration test → deploy

- **Lint** — flake8 (Python), eslint (JavaScript), hadolint (Dockerfiles)
- **Test** — pytest with Redis mocked, coverage report uploaded as artifact
- **Build** — builds all three images, tags with git SHA and latest, pushes
  to a local registry
- **Security scan** — Trivy scans all images, fails on any CRITICAL CVE,
  uploads SARIF artifact
- **Integration test** — spins up the full stack, submits a real job, polls
  until complete, tears down cleanly
- **Deploy** — SSH rolling update to EC2, new container must pass healthcheck
  before old one is stopped

---

## Stopping the Stack

```bash
docker-compose down
```

To also remove volumes (clears Redis data):

```bash
docker-compose down -v
```

---

## Environment Variables

See `.env.example` for all required variables and descriptions.

---

## Bug Fixes

See [FIXES.md](./FIXES.md) for a full list of every bug found in the starter
repository, including file, line number, problem description, and fix applied.
