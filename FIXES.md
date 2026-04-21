# FIXES.md

This document records every bug found in the starter repository, including the file, line number, nature of the problem, and the fix applied.

---

## Fix 1 — Hardcoded Redis hostname in API

**File:** `api/main.py`  
**Line:** 8  
**Problem:** The Redis client was created with `host="localhost"`, which works when running directly on a host machine but fails when the service runs inside a Docker container. Containers cannot reach each other via `localhost`; they communicate using Docker's internal DNS, resolved by service name.  
**Fix:** Replaced `host="localhost"` with `host=os.environ.get("REDIS_HOST", "redis")` so the hostname is read from an environment variable, with `"redis"` as the default (matching the Docker Compose service name).

---

## Fix 2 — Redis password never used in API connection

**File:** `api/main.py`  
**Line:** 8  
**Problem:** The `.env` file defined `REDIS_PASSWORD`, but the `redis.Redis(...)` constructor in `main.py` did not pass a `password` argument. If Redis is configured to require authentication, the connection would be rejected with an `AUTHFAILED` error.  
**Fix:** Added `password=os.environ.get("REDIS_PASSWORD")` to the Redis constructor call.

---

## Fix 3 — Hardcoded Redis hostname in worker

**File:** `worker/worker.py`  
**Line:** 6  
**Problem:** Same issue as Fix 1. The worker used `host="localhost"`, which breaks in a containerised environment.  
**Fix:** Replaced with `host=os.environ.get("REDIS_HOST", "redis")` and also added `port=int(os.environ.get("REDIS_PORT", 6379))`.

---

## Fix 4 — Redis password never used in worker connection

**File:** `worker/worker.py`  
**Line:** 6  
**Problem:** Same issue as Fix 2. The worker connected to Redis without sending the password.  
**Fix:** Added `password=os.environ.get("REDIS_PASSWORD")` to the Redis constructor call.

---

## Fix 5 — Unused import in worker

**File:** `worker/worker.py`  
**Line:** 4  
**Problem:** `import signal` was present but the `signal` module was never used anywhere in the file. This is dead code and would cause a `flake8` lint failure (F401: imported but unused).  
**Fix:** Removed the unused `import signal` line.

---

## Fix 6 — Hardcoded API URL in frontend

**File:** `frontend/app.js`  
**Line:** 6  
**Problem:** `const API_URL = "http://localhost:8000"` was hardcoded. When the frontend runs inside a Docker container, `localhost` refers to the frontend container itself, not the API container. The API would be unreachable, causing all job submission and status requests to fail.  
**Fix:** Replaced with `const API_URL = process.env.API_URL || "http://api:8000"` so the URL is read from an environment variable, defaulting to the Docker Compose API service name.

---

## Fix 7 — Real credentials committed to the repository

**File:** `api/.env`  
**Line:** 1  
**Problem:** The `.env` file containing `REDIS_PASSWORD=supersecretpassword123` was committed to the repository. Committing secrets to version control is a critical security vulnerability.  
**Fix:** Removed `api/.env` from git tracking using `git rm --cached api/.env`, added `.env` to `.gitignore`, and created `api/.env.example` with placeholder values to document required variables without exposing secrets.

---

## Fix 8 — Missing .gitignore

**File:** `.gitignore` (missing — did not exist)  
**Line:** N/A  
**Problem:** The repository had no `.gitignore` file, meaning `.env` files, `__pycache__`, `node_modules`, and other generated files could be accidentally committed.  
**Fix:** Created a `.gitignore` at the repository root with at minimum `.env` listed to prevent secret files from being tracked.

---

## Fix 9 — Unpinned dependency versions in API

**File:** `api/requirements.txt`  
**Lines:** 1–3  
**Problem:** All three dependencies (`fastapi`, `uvicorn`, `redis`) had no version pins. This breaks reproducibility — a fresh `pip install` at a later date could pull in a breaking newer version and fail silently.  Also, `uvicorn` was listed without the `[standard]` extras, missing performance-critical dependencies (`uvloop`, `httptools`).  
**Fix:** Pinned all versions (`fastapi==0.104.1`, `uvicorn[standard]==0.24.0`, `redis==5.0.1`). Created a separate `api/requirements-test.txt` for test-only dependencies (`pytest`, `httpx`, `pytest-cov`) to keep production and test dependencies cleanly separated.

---

## Fix 10 — Unpinned dependency version in worker

**File:** `worker/requirements.txt`  
**Line:** 1  
**Problem:** `redis` had no version pin, creating the same reproducibility problem as Fix 9.  
**Fix:** Pinned to `redis==5.0.1` to match the version used by the API service.

## Fix 11 — Hardcoded port in frontend server

**File:** `frontend/app.js`  
**Line:** 30 
**Problem:** The port was hardcoded as `3000` directly in `app.listen(3000, ...)`. This means the port can never be changed without editing source code, which is bad practice for a containerised service where configuration should come from environment variables.  
**Fix:** Replaced with `const PORT = process.env.PORT || 3000;` and updated the listen call to `app.listen(PORT, ...)` so the port is configurable via environment variable with `3000` as the default.

## Fix 12 — Unused error variable in frontend catch blocks

**File:** `frontend/app.js`  
**Lines:** 16, 25  
**Problem:** Both catch blocks captured the `err` variable but never used it, always returning a generic hardcoded error message regardless of what actually went wrong. This caused ESLint warnings and meant errors were silently swallowed with no useful information returned to the caller.  
**Fix:** Replaced the hardcoded `"something went wrong"` string with `err.message` so the actual error is returned in the response.

## Fix 13 — Flake8 violations in API and test files

**File:** `api/main.py`  
**Lines:** 22, 29, 33  
**Problem:** Missing two blank lines before function definitions (E302) and no newline at end of file (W292). PEP8 requires two blank lines between top-level function definitions.  
**Fix:** Added two blank lines before each route function and added a newline at the end of the file.

---

**File:** `api/tests/test_main.py`  
**Lines:** 1, 58  
**Problem:** `import pytest` was present but never used (F401), and no newline at end of file (W292).  
**Fix:** Removed the unused `import pytest` line and added a newline at the end of the file.

## Fix 14 — Flake8 violations in worker

**File:** `worker/worker.py`  
**Lines:** 19, 23  
**Problem:** Missing two blank lines after function definition (E305) and no newline at end of file (W292). PEP8 requires two blank lines between top-level function definitions and module-level code.  
**Fix:** Added two blank lines after `process_job` function definition and added a newline at the end of the file.

4. Document It

A README.md that explains how to bring the entire stack up on a clean machine from scratch—list prerequisites, all commands, and what a successful startup looks like
A FIXES.md documenting every bug found—file, line number, what it was, and how you fixed it
A .env.example committed with placeholder values for every required variable
Evaluation Criteria / Acceptance Criteria
Your fork must be public. Private repositories will not be graded
Everything must be committed—nothing should only exist locally
.env must never appear in your repository or git history. This will cost you heavily
Do not hardcode secrets, passwords, or tokens anywhere—YAML files, Python, JavaScript, or git history all count
No cloud accounts required. This task runs entirely on your machine and GitHub's free tier
Do not open a pull request to the starter repo

## Fix 16 — Critical CVEs in frontend Docker image

**File:** `frontend/Dockerfile`  
**Line:** Final stage  
**Problem:** Alpine 3.21.3 shipped with `libcrypto3` and `libssl3` at version `3.3.3-r0`, which contains CVE-2025-15467 — a CRITICAL OpenSSL vulnerability allowing remote code execution or denial of service. Trivy flagged this and failed the pipeline.  
**Fix:** Added `RUN apk upgrade --no-cache` to the final stage so Alpine upgrades all packages including `libcrypto3` and `libssl3` to their patched versions at build time.

---
