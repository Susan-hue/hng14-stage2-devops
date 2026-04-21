import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

with patch("redis.Redis") as mock_redis:
    mock_redis.return_value = MagicMock()
    from main import app

client = TestClient(app)


# ── Test 1 — Health endpoint returns 200 ─────────────────
def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# ── Test 2 — Creating a job returns 200 and a job_id ─────
def test_create_job():
    with patch("main.r") as mock_r:
        mock_r.lpush = MagicMock(return_value=1)
        mock_r.hset = MagicMock(return_value=1)

        response = client.post("/jobs")

        assert response.status_code == 200
        data = response.json()
        assert "job_id" in data


# ── Test 3 — Getting a job status returns correct data ───
def test_get_job_status():
    with patch("main.r") as mock_r:
        mock_r.hget = MagicMock(return_value=b"queued")

        response = client.get("/jobs/test-123")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "queued"
        assert data["job_id"] == "test-123"


# ── Test 4 — Getting a job that doesn't exist returns error
def test_get_nonexistent_job():
    with patch("main.r") as mock_r:
        mock_r.hget = MagicMock(return_value=None)

        response = client.get("/jobs/doesnotexist")

        assert response.status_code == 200
        data = response.json()
        assert data["error"] == "not found"