<h3 align="center">🛠️ rural-ortho-link</h3>

<div align="center">
  <a href="https://github.com/axentx/rural-ortho-link/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT">
  </a>
  <a href="https://github.com/axentx/rural-ortho-link">
    <img src="https://img.shields.io/badge/Language-Python-blue.svg" alt="Language: Python">
  </a>
  <a href="https://github.com/axentx/rural-ortho-link/actions">
    <img src="https://img.shields.io/github/actions/workflow/status/axentx/rural-ortho-link/build.yml?branch=main" alt="Build Status">
  </a>
  <a href="https://github.com/axentx/rural-ortho-link/stargazers">
    <img src="https://img.shields.io/github/stars/axentx/rural-ortho-link?style=social" alt="Stars">
  </a>
</div>

---
# 🚀 rural-ortho-link
**Power rural healthcare clinics with secure, low-bandwidth teleconsultations.** rural-ortho-link is a telehealth platform enabling low‑bandwidth, secure orthopedic video consultations for rural clinics.

## Why rural-ortho-link?
* **Secure**: Provides JWT/OAuth2 authentication for secure video consultations
* **Low-bandwidth**: Optimized for 3G/4G networks, enabling video calls in rural areas
* **Specialist marketplace**: Connects rural healthcare clinics with orthopedic specialists
* **Image sharing**: Allows for X-ray and MRI image upload and sharing
* **Analytics dashboards**: Provides insights into consultation metrics and patient data
* **EHR integration**: Supports REST hooks for integration with Electronic Health Records (EHR) systems
* **Scalable**: Built with FastAPI and WebRTC for efficient and scalable video streaming

## Feature Overview
| Feature | Description |
| --- | --- |
| Video Consultations | Secure, low-bandwidth video calls for orthopedic consultations |
| Authentication | JWT/OAuth2 authentication for secure login and authorization |
| Image Sharing | Upload and share X-ray and MRI images for consultation purposes |
| Specialist Marketplace | Connects rural healthcare clinics with orthopedic specialists |
| Analytics Dashboards | Provides insights into consultation metrics and patient data |
| EHR Integration | Supports REST hooks for integration with Electronic Health Records (EHR) systems |

## Tech Stack
* Python
* FastAPI
* WebRTC
* JWT
* OAuth2

## Project Structure
* `business`: Business-related documents and artifacts
* `docs`: Documentation for the project
* `src`: Source code for the application
* `tests`: Test suite for the application

## Getting Started
```bash
# Install dependencies
poetry install

# Run the application
poetry run uvicorn main:app --host 0.0.0.0 --port 8000

# Run tests
poetry run pytest
```

## Deploy
```bash
# Build the Docker image
docker build -t rural-ortho-link .

# Run the Docker container
docker run -p 8000:8000 rural-ortho-link
```

## Status
Last commit: `e16e4b3` - style: [DECISION] docs cycle 20260619-150032-rural-or

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on contributing to rural-ortho-link.

## License
rural-ortho-link is licensed under the MIT License. See [LICENSE](LICENSE) for details.