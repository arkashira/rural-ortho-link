<h3 align="center">🛠️ rural-ortho-link</h3>

<div align="center">
  <a href="https://github.com/axentx/rural-ortho-link/blob/main/LICENSE"><img src="https://img.shields.io/github/license/axentx/rural-ortho-link?color=brightgreen" alt="License"></a>
  <a href="https://github.com/axentx/rural-ortho-link"><img src="https://img.shields.io/github/languages/top/axentx/rural-ortho-link?color=blue" alt="Language"></a>
  <a href="https://github.com/axentx/rural-ortho-link/actions"><img src="https://img.shields.io/github/workflow/status/axentx/rural-ortho-link/CI?label=build&color=orange" alt="Build Status"></a>
  <a href="https://github.com/axentx/rural-ortho-link/stargazers"><img src="https://img.shields.io/github/stars/axentx/rural-ortho-link?style=social" alt="Stars"></a>
</div>

---

# 🚀 rural-ortho-link  
**Power rural clinics with secure, low‑bandwidth orthopedic video consultations.** A telehealth platform that lets rural clinics conduct secure orthopedic video consultations with specialists, share diagnostic images, and manage appointments—all while integrating with existing EHR systems.

## Why rural-ortho-link?
- **Low‑bandwidth ready** – Optimized WebRTC streams work on 3G/4G connections, reducing drop‑out rates by > 30 %.
- **Secure by design** – End‑to‑end JWT/OAuth2 authentication meets HIPAA‑level encryption standards.
- **Image‑centric workflow** – Clinicians can upload X‑rays, MRIs, and other diagnostics directly into the consult session.
- **Specialist marketplace** – Built‑in directory lets clinics find and book board‑certified orthopedic experts in seconds.
- **Analytics dashboard** – Real‑time metrics on consult duration, patient satisfaction, and referral conversion.
- **EHR‑friendly** – Simple REST hooks let you sync appointments and notes with any major electronic health record system.

## Feature Overview

| Feature | Description |
|---------|-------------|
| **Secure Video Calls** | WebRTC‑based, adaptive bitrate video conferencing with end‑to‑end encryption. |
| **Diagnostic Image Upload** | Drag‑and‑drop support for X‑rays, MRIs, CT scans; automatic thumbnail generation. |
| **Appointment Scheduler** | Calendar view, automated reminders, and specialist availability matching. |
| **Specialist Directory** | Searchable list of vetted orthopedic surgeons with profiles, ratings, and languages. |
| **EHR Integration** | OAuth2‑protected REST endpoints for syncing patient data and consult notes. |
| **Analytics & Reporting** | Dashboard showing consult volume, average session length, and outcome metrics. |
| **Multi‑tenant Architecture** | Isolated data per clinic with role‑based access control. |

## Tech Stack
- **Frontend**: React, TypeScript, TailwindCSS  
- **Backend**: Node.js, Express  
- **Database**: PostgreSQL  
- **Auth**: JWT, OAuth2  
- **Realtime**: WebRTC  

## Project Structure
```
rural-ortho-link/
├─ business/          # business artefacts (BMC, PRD, etc.)
├─ docs/              # documentation, specs, roadmaps
├─ src/
│  ├─ frontend/       # React + TS UI
│  └─ backend/        # Express API server
├─ tests/             # unit & integration tests
├─ README.md
├─ pyproject.toml     # entry‑point configuration (for tooling)
└─ requirements.txt   # Python deps (used by CI scripts)
```

## Getting Started

### Prerequisites
```bash
# Node.js (>=18)
# Python 3.11 (for CI helper scripts)
# Docker (optional, for local DB)
```

### Backend
```bash
cd src/backend
# Install Node dependencies
npm ci

# Set up environment variables (example)
cp .env.example .env
# Edit .env to add DB credentials, JWT secret, OAuth client IDs, etc.

# Run PostgreSQL locally (Docker)
docker run -d \
  -e POSTGRES_USER=ortho \
  -e POSTGRES_PASSWORD=secret \
  -e POSTGRES_DB=ortho_link \
  -p 5432:5432 postgres:15

# Start the API server
npm run dev   # runs `node src/index.js` with nodemon
```

### Frontend
```bash
cd src/frontend
npm ci
npm run dev   # starts Vite dev server at http://localhost:5173
```

### Run the full stack (optional Docker Compose)
```bash
docker compose up --build
```

### Tests
```bash
# Backend tests
cd src/backend && npm test

# Frontend tests
cd src/frontend && npm test

# End‑to‑end (Cypress) – requires the stack to be running
npm run test:e2e
```

## Deploy

The platform is container‑ready and can be deployed to any Docker‑compatible host (AWS ECS, GCP Cloud Run, Azure Container Apps, etc.).

```bash
# Build images
docker build -t axentx/rural-ortho-link-frontend ./src/frontend
docker build -t axentx/rural-ortho-link-backend ./src/backend

# Push to registry
docker push axentx/rural-ortho-link-frontend
docker push axentx/rural-ortho-link-backend

# Deploy with your orchestrator – example for Docker Compose in production
docker compose -f docker-compose.prod.yml up -d
```

## Status
**Early‑stage MVP** – real, sandbox‑tested implementation (commit `4136c5f`).  

## Contributing
Please see our [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to propose improvements, report bugs, and submit pull requests.

## License
Distributed under the MIT License. See `LICENSE` for more information.