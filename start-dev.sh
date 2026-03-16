#!/bin/bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$REPO_ROOT/backend"
FRONTEND_DIR="$REPO_ROOT/frontend"
FRONTEND_PORT=4173
BACKEND_PORT=8000

cleanup() {
  if [[ -n "${BACKEND_PID:-}" ]]; then
    echo "Stopping backend (pid $BACKEND_PID)..."
    kill "$BACKEND_PID" >/dev/null 2>&1 || true
  fi
}
trap cleanup EXIT

if ! command -v npm >/dev/null 2>&1; then
  echo "npm is required to run the frontend. Install Node.js/npm or rebuild the devcontainer first."
  exit 1
fi

if ! command -v python >/dev/null 2>&1; then
  echo "Python is required to run the backend. Install Python 3.10+ before continuing."
  exit 1
fi

wait_for_backend() {
  local retries=12
  local delay=0.5

  echo "Waiting for backend to be ready on http://localhost:$BACKEND_PORT..."
  for ((i=1; i<=retries; i++)); do
    if curl -fsS "http://localhost:$BACKEND_PORT/health" >/dev/null 2>&1; then
      echo "Backend ready."
      return 0
    fi
    sleep "${delay}"
  done

  echo "Backend did not become healthy within $((retries * delay)) seconds."
  return 1
}

cd "$BACKEND_DIR"
python main.py &
BACKEND_PID=$!

wait_for_backend

cd "$FRONTEND_DIR"
npm install

npm run dev -- --host 0.0.0.0 --port $FRONTEND_PORT
