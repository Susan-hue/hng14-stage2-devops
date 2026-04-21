#!/bin/bash
set -e

TIMEOUT=60
ELAPSED=0
INTERVAL=3

echo "Submitting a job..."
RESPONSE=$(curl -s -X POST http://localhost:3000/submit \
  -H "Content-Type: application/json")
echo "Submit response: $RESPONSE"

JOB_ID=$(echo $RESPONSE | python3 -c \
  "import sys,json; print(json.load(sys.stdin)['job_id'])")
echo "Job ID: $JOB_ID"

echo "Polling for job completion (timeout: ${TIMEOUT}s)..."
for i in $(seq 1 20); do
  STATUS=$(curl -s http://localhost:3000/status/$JOB_ID | \
    python3 -c "import sys,json; print(json.load(sys.stdin)['status'])")
  echo "Attempt $i — status: $STATUS"
  if [ "$STATUS" = "completed" ]; then
    echo "Job completed successfully"
    exit 0
  fi
  ELAPSED=$((ELAPSED + INTERVAL))
  if [ $ELAPSED -ge $TIMEOUT ]; then
    echo "Job did not complete within ${TIMEOUT} seconds"
    exit 1
  fi
  sleep $INTERVAL
done

echo "Job did not complete within 60 seconds"
exit 1