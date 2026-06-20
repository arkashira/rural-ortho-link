<h3 align="center">🛠️ rural-ortho-link</h3>

<div align="center">
  <a href="https://github.com/your-org/rural-ortho-link/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License: MIT"></a>
  <a href="https://github.com/your-org/rural-ortho-link"><img src="https://img.shields.io/github/languages/top/your-org/rural-ortho-link?color=blue&logo=python&logoColor=white" alt="Language: Python"></a>
  <a href="https://github.com/your-org/rural-ortho-link/actions"><img src="https://img.shields.io/github/workflow/status/your-org/rural-ortho-link/CI?label=build" alt="Build Status"></a>
  <a href="https://github.com/your-org/rural-ortho-link/stargazers"><img src="https://img.shields.io/github/stars/your-org/rural-ortho-link?style=social" alt="Stars"></a>
</div>

---  

# 🚀 rural-ortho-link  
**Power rural clinics with low‑bandwidth, secure orthopedic video consultations.** A tele‑health platform that brings specialist care to remote patients without the need to travel.

## Why rural-ortho-link?  

- **Zero‑Travel Savings** – Rural patients save an average of **$250 USD (≈ 8,750 THB) per visit** by consulting from their local clinic.  
- **Low‑Bandwidth Ready** – WebRTC streams are **optimised for 3G/4G**, guaranteeing smooth video even on spotty connections.  
- **Secure Access** – **JWT + OAuth2** authentication ensures HIPAA‑grade data protection.  
- **Full Imaging Support** – Upload and share **X‑rays, MRIs, and other scans** directly within the consultation.  
- **Specialist Marketplace** – Connects clinics with **board‑certified orthopedic surgeons** on demand.  
- **Analytics Dashboard** – Real‑time usage & outcome metrics help clinics improve care pathways.  
- **EHR Integration** – REST hooks let you **sync notes and images** with existing electronic health records.  

## Feature Overview  

| Feature | Description |
|---------|-------------|
| **WebRTC Video Calls** | Adaptive bitrate streaming for 3G/4G, peer‑to‑peer via FastAPI WebSockets. |
| **Auth & Permissions** | JWT‑based session tokens + OAuth2 provider support (Google, Azure AD). |
| **Image Upload** | Secure, chunked upload of large DICOM files; preview in‑call. |
| **Specialist Marketplace** | searchable directory, availability calendar, booking API. |
| **Analytics Dashboard** | KPI widgets (consults per week, bandwidth usage, patient satisfaction). |
| **EHR Hooks** | Configurable outbound webhooks for encounter data, imaging links. |
| **Background Tasks** | Celery‑style async jobs for analytics aggregation and email notifications. |

## Tech Stack  

- **Python** – Core language, type‑checked with `mypy`.  
- **FastAPI** – High‑performance API layer & WebSocket handling.  
- **WebRTC** – Real‑time video/audio transport, tuned for low‑bandwidth.  
- **JWT** – Stateless authentication tokens.  
- **OAuth2** – Third‑party identity provider integration.  
- **Poetry** – Dependency management & packaging.  
- **Pytest** – Test runner for unit & integration tests.  

## Project Structure  

```
rural-ortho-link/
├─ business/          # Business logic, domain models
├─ docs/              # Documentation assets
├─ src/               # Application source code
│  ├─ api/            # FastAPI routers & WebSocket endpoints
│  ├─ core/           # Auth, settings, utilities
│  └─ services/       # Video, imaging, analytics services
├─ tests/             # Pytest test suite
├─ pyproject.toml     # Poetry config & entry points
├─ requirements.txt   # Pin‑file for CI environments
└─ README.md
```

## Getting Started  

```bash
# 1️⃣ Clone the repo
git clone https://github.com/your-org/rural-ortho-link.git
cd rural-ortho-link

# 2️⃣ Install dependencies with Poetry
poetry install

# 3️⃣ Run database migrations (if any)
poetry run alembic upgrade head   # optional, depends on your DB setup

# 4️⃣ Start the development server
poetry run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

The API docs are then available at: `http://localhost:8000/docs`

### Running Tests  

```bash
poetry run pytest -vv
```

## Deploy  

The project ships with a Dockerfile ready for production. Example deployment to a container host:

```bash
# Build the image
docker build -t rural-ortho-link:latest .

# Run the container (replace <SECRET_KEY> with your JWT secret)
docker run -d \
  -e JWT_SECRET_KEY=<SECRET_KEY> \
  -e OAUTH2_CLIENT_ID=<CLIENT_ID> \
  -e OAUTH2_CLIENT_SECRET=<CLIENT_SECRET> \
  -p 80:8000 \
  rural-ortho-link:latest
```

For Kubernetes, use the provided `k8s/` manifests (not shown here) and apply with `kubectl apply -k k8s/`.

## Status  

🚧 **Early stage** – core video & auth flows are functional; sandbox testing completed.  
_Last commit: `b33ff59` – real, sandbox‑tested implementation (2026‑06‑19)._

## Contributing  

We welcome contributions! Please read our [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to propose changes, run tests, and submit pull requests.

## License  

This project is licensed under the **MIT License**.