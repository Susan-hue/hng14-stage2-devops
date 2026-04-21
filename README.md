# Stage 2 DevOps — Containerized Job Processing System

A multi-service job processing system containerized with Docker and deployed
via a full CI/CD pipeline using GitHub Actions.

---

## Services

| Service | Technology | Role |
|---|---|---|
| Frontend | Node.js/Express | Users submit and track jobs |
| API | Python/FastAPI | Creates jobs and serves status updates |
| Worker | Python | Picks up and processes jobs from the queue |
| Redis | Redis 7 | Shared message queue between API and worker |

---

## Prerequisites

| Tool | Minimum Version |
|---|---|
| Docker | v20+ |
| Docker Compose | v1.29+ |
| Git | Any recent version |

---

## Quickstart

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

### 4. Verify all services are healthy

```bash
docker-compose ps
```

Expected output:

Name              Command               State                Ports

app_api_1        uvicorn main:app ...          Up (healthy)     8000/tcp
app_frontend_1   node app.js                   Up (healthy)     0.0.0.0:3000->3000/tcp
app_redis_1      docker-entrypoint.sh ...      Up (healthy)     6379/tcp
app_worker_1     python worker.py              Up (healthy)

All four services must show `Up (healthy)` before the application is ready.

### 5. Open the application

http://localhost:3000

---

## Verifying Each Service

**Check API health:**
```bash
curl http://localhost:8000/health
# Expected: {"status": "ok"}
```

**Submit a job:**
```bash
curl -X POST http://localhost:3000/submit
# Expected: {"job_id": "<uuid>"}
```

**Check job status:**
```bash
curl http://localhost:3000/status/<job_id>
# Expected: {"job_id": "<uuid>", "status": "completed"}
```

---

## CI/CD Pipeline

Runs automatically on every push to `main` via GitHub Actions.

lint → test → build → security scan → integration test → deploy

| Stage | What it does |
|---|---|
| Lint | flake8 (Python), eslint (JavaScript), hadolint (Dockerfiles) |
| Test | pytest with Redis mocked, coverage report uploaded as artifact |
| Build | Builds all three images, tags with git SHA and latest, pushes to local registry |
| Security scan | Trivy scans all images, fails on any CRITICAL CVE, uploads SARIF artifact |
| Integration test | Spins up full stack, submits real job, polls until complete, tears down cleanly |
| Deploy | SSH rolling update to EC2 — new container must pass healthcheck before old one stops |

A failure in any stage prevents all subsequent stages from running.

---

## Stopping the Stack

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (clears Redis data)
docker-compose down -v
```

---

## Environment Variables

See [`.env.example`](./.env.example) for all required variables with descriptions.

---

## Bug Fixes

See [`FIXES.md`](./FIXES.md) for every bug found in the starter repository,
including file, line number, problem description, and fix applied.