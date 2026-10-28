# Deploy Project Quantum-Grav

The public app remains on GitHub Pages. The FastAPI service runs separately on Render and writes calculation telemetry to Supabase. Share/open the GitHub Pages URL as the app link; the pages call the Render API in the background.

## 1. Set the Supabase connection string

In Supabase, open **Project Settings → Database → Connection string → URI** and copy the URI. Use the pooler connection string if your host requires IPv4. Keep the password private; do not put it in this repository or in `api-config.js`.

## 2. Publish the backend

Commit and push the project changes to the GitHub repository connected to the project. In Render, create a **New + → Blueprint** from that repository and select `render.yaml`. In the service environment settings, add `DATABASE_URL` with the Supabase URI. Set `FRONTEND_ORIGINS` to the exact GitHub Pages origin, for example `https://jdilshan051-design.github.io` (no path and no trailing slash). The service starts with `api.app:app`; on first startup it creates the `flight_logs` table.

After deployment, open `https://<your-render-service>.onrender.com/health`. It should return `{"status":"ok","database_connected":true}`.

## 3. Point the GitHub Pages frontend at the API

Edit `api-config.js` and replace `https://YOUR-BACKEND.onrender.com` with the actual Render service URL, without a trailing slash. Commit and push that change. GitHub Pages redeploys the static frontend; the existing Pages URL remains the link to share.

The API docs are available at `https://<your-render-service>.onrender.com/docs`. Calculation requests from Phase 5 are stored in Supabase; the Phase 2–4 interactive calculations use the matching backend endpoints.

## Secrets

Never commit the Supabase connection string. Store it only as Render's `DATABASE_URL` environment variable. If it was ever committed or shared, rotate the database password in Supabase.
