# Frontend Application

This directory contains the React + Vite frontend for the project. It is styled with Tailwind CSS and wired for the PromptLab FastAPI backend.

## Getting Started

1. **Install dependencies:**

   ```bash
   cd frontend
   npm install
   ```

2. **Start the backend API** (from the repo root):

   ```bash
   cd backend
   python main.py
   ```

   The FastAPI server listens on `http://localhost:8000` by default and exposes `/prompts` and `/collections` resources.

3. **Run the frontend**:

   ```bash
   cd frontend
   npm run dev -- --host 0.0.0.0 --port 4173
   ```

   Use the VS Code Ports view or your browser to open the forwarded port.

> **Note:** Node.js/npm must be installed in the environment where you run the frontend (the devcontainer rebuild installs Node automatically).

## API integration

- `src/api/client.js` centralizes the base URL (`VITE_API_URL`, defaulting to `http://localhost:4000/api`) and serializes JSON, errors, and query params.
- `src/api/prompts.js` and `src/api/collections.js` wrap the FastAPI endpoints: `GET /prompts`, `POST /prompts`, `PUT /prompts/{id}`, `DELETE /prompts/{id}`, `GET /collections`, `POST /collections`, `DELETE /collections/{id}`.
- Update `frontend/.env` (copy from `.env.example` if present) to point `VITE_API_URL` at your running backend (e.g., `VITE_API_URL=http://localhost:8000`).

## Styling

- Tailwind CSS is configured via `tailwind.config.js`, `postcss.config.js`, and `src/styles/globals.css`.
- Add or customize utility classes directly in components or define new ones inside the global styles file.

## Available Scripts

- `npm run dev`: Start the Vite development server.
- `npm run build`: Bundle the app for production.
- `npm run preview`: Preview the production build locally.
- `npm run test:e2e`: Run the Playwright end-to-end suite against `http://localhost:4173`.

## Playwright end-to-end tests

The project now includes a lightweight Playwright suite that interacts with the real UI/API stack (health badge, prompt form, collection form) to keep key flows verified.

1. Start the backend + frontend manually (use `./start-dev.sh` or run `npm run dev` while the backend is already running on `http://localhost:8000`).
2. From the `frontend/` directory install dependencies if you haven’t already:

   ```bash
   npm install
   npx playwright install --with-deps
   ```

3. Run the tests:

   ```bash
   npm run test:e2e
   ```

   Playwright spins up Chromium, navigates the UI, creates a prompt and a collection, and asserts the results appear in the dashboard. Logs and failure artifacts are available in the generated `playwright-report/` directory (`npx playwright show-report`).

> Tip: set `PLAYWRIGHT_BASE_URL` to point at a deployed frontend if you want to run the same suite against staging or preview environments.
