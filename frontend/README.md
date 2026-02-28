# PromptLab Frontend

This is a minimal Vite + React frontend for PromptLab.

Prerequisites:
- Node.js 18+ / npm or pnpm

Run locally:

```bash
cd frontend
npm install
npm run dev
```

The app expects the backend API at `http://127.0.0.1:8000` by default. To change the API URL, set `VITE_API_URL` in your environment when running Vite.

Notes:
- This is a small development scaffold intended to be extended. It supports listing prompts, creating prompts, patching (editing) and deleting prompts, and simple collection management.
- For production builds run `npm run build`.
