# TECH_SPEC.md  

**Project:** rural-ortho-link  
**Owner:** AxentX – Telemedicine Division  
**Status:** MVP (ready for development)  
**Last Updated:** 2026‑06‑16  

---  

## 1. Overview  

rural-ortho-link is a tele‑medicine platform that connects patients in underserved rural areas with board‑certified orthopedic specialists. The system enables:  

* Secure video/voice consultations.  
* Structured capture of clinical data (history, imaging, functional scores).  
* Generation and electronic delivery of **off‑label therapy prescriptions** (e.g., compounded biologics, custom orthotics).  
* Integration with local primary‑care EMR systems for referral and follow‑up.  

The product must comply with **HIPAA**, **GDPR** (for EU‑based patients), and **FDA** regulations for off‑label prescribing.  

---  

## 2. Architecture Overview  

```
+-------------------+       +-------------------+       +-------------------+
|   Front‑End (Web) | <---> |   API Gateway     | <---> |   Auth Service    |
+-------------------+       +-------------------+       +-------------------+
                                 |
                                 v
                         +-------------------+
                         |   Service Mesh    |
                         +-------------------+
                                 |
        +------------------------+------------------------+
        |                        |                        |
        v                        v                        v
+----------------+      +----------------+      +-------------------+
|  Consultation  |      |  Prescription  |      |  Integration Hub  |
|  Service       |      |  Service       |      |  (FHIR/HL7)       |
+----------------+      +----------------+      +-------------------+
        |                        |                        |
        v                        v                        v
+----------------+      +----------------+      +-------------------+
|  Media Service |      |  Document Gen  |      |  EMR Connectors   |
|  (vLLM/Live)   |      |  Service       |      |  (FHIR, HL7)      |
+----------------+      +----------------+      +-------------------+

```

* **API Gateway** – Kong (open‑source) with JWT/OAuth2 enforcement.  
* **Service Mesh** – Istio for mTLS, traffic routing, observability.  
* **Data Store** – PostgreSQL (clinical data) + MongoDB (unstructured media).  
* **Search** – ElasticSearch for patient‑record lookup.  
* **Streaming Media** – WebRTC powered by Janus Gateway; fallback to HLS.  
* **LLM‑assisted Documentation** – vLLM inference engine (GPU‑accelerated) for generating prescription narratives and discharge summaries.  
* **CI/CD** – GitHub Actions + ArgoCD (GitOps).  

---  

## 3. Core Components  

| Component | Responsibility | Tech Stack | Key Interfaces |
|-----------|----------------|------------|----------------|
| **Auth Service** | Identity & access management, token issuance, role‑based ACLs (Patient, Provider, Admin). | Keycloak (Docker), PostgreSQL | `/auth/login`, `/auth/refresh`, `/auth/logout` |
| **Consultation Service** | Schedule, start, and record video visits; store session metadata. | Go (gRPC), Janus, Redis (session cache) | `POST /consultations`, `GET /consultations/{id}`, `WebSocket /consultations/{id}/stream` |
| **Prescription Service** | Validate off‑label therapy rules, generate structured prescription objects, sign with provider’s digital certificate. | Python (FastAPI), vLLM, PostgreSQL | `POST /prescriptions`, `GET /prescriptions/{id}` |
| **Document Generation Service** | Render PDFs/HTML for discharge summaries, consent forms, and e‑prescriptions. | Node.js (NestJS), Puppeteer, LaTeX templates | `POST /documents/render` |
| **Integration Hub** | Translate internal models to FHIR resources, push/pull to partner EMRs. | Java (Spring Boot), HAPI‑FHIR, HL7 v2 bridge | `POST /fhir/Patient`, `GET /hl7/Observation` |
| **Media Service** | Record & store encrypted video/audio streams; provide playback links. | MinIO (S3‑compatible), AES‑256‑GCM, FFmpeg | `GET /media/{id}` |
| **Analytics & Auditing** | Event logging, compliance audit trails, usage metrics. | ElasticSearch + Kibana, OpenTelemetry | – |

---  

## 4. Data Model  

### 4.1 Relational (PostgreSQL)

| Table | Primary Key | Important Columns |
|-------|--------------|-------------------|
| `users` | `user_id` (UUID) | `email`, `hashed_pw`, `role`, `created_at` |
| `patients` | `patient_id` (UUID) | `user_id`, `demographics JSONB`, `address`, `insurance_id` |
| `providers` | `provider_id` (UUID) | `user_id`, `license_number`, `specialty`, `cert_key` |
| `consultations` | `consultation_id` (UUID) | `patient_id`, `provider_id`, `scheduled_at`, `status`, `media_ref` |
| `prescriptions` | `prescription_id` (UUID) | `consultation_id`, `provider_id`, `patient_id`, `therapy_code`, `dosage_json`, `signed_blob`, `valid_until` |
| `audit_logs` | `log_id` (bigserial) | `entity_type`, `entity_id`, `action`, `actor_id`, `timestamp`, `details JSONB` |

### 4.2 Document Store (MongoDB)

* `media_chunks` – encrypted video/audio segments (gridFS).  
* `clinical_notes` – free‑text notes, LLM‑generated drafts (versioned).  

### 4.3 FHIR Mapping (Integration Hub)

| Internal Entity | FHIR Resource |
|-----------------|---------------|
| Patient → `Patient` |
| Provider → `Practitioner` |
| Consultation → `Encounter` |
| Prescription → `MedicationRequest` (with `extension` for off‑label flag) |
| Clinical Notes → `Observation` (type = “clinical-note”) |

---  

## 5. Key APIs / Interfaces  

All external APIs are versioned under `/api/v1/`.  

### 5.1 Authentication  

```http
POST /api/v1/auth/login
{
  "email": "user@example.com",
  "password": "••••••"
}
```

Returns JWT (access) + refresh token.  

### 5.2 Consultation  

```http
POST /api/v1/consultations
{
  "patient_id": "uuid",
  "provider_id": "uuid",
  "scheduled_at": "2026-07-01T14:00:00Z"
}
```

*Response:* `consultation_id`, `join_url` (WebRTC token).  

WebSocket endpoint for real‑time signaling:  

```
wss://api.axentx.com/consultations/{consultation_id}/ws
```  

### 5.3 Prescription  

```http
POST /api/v1/prescriptions
{
  "consultation_id": "uuid",
  "therapy_code": "BIO-001",
  "dosage": { "amount": "5ml", "frequency": "q.d." },
  "patient_consent": true
}
```

Server validates off‑label policy (rule engine stored in PostgreSQL `off_label_rules`).  

Response includes signed PDF URL (temporary signed S3 link).  

### 5.4 Integration  

```http
POST /api/v1/fhir/MedicationRequest
Content-Type: application/fhir+json
{
  ...FHIR payload...
}
```

Bidirectional sync is handled via background workers (Kafka topics `fhir.outbound`, `fhir.inbound`).  

---  

## 6. Technology Stack  

| Layer | Choice | Rationale |
|-------|--------|-----------|
| **API Gateway** | Kong (Docker) | Mature plugin ecosystem (auth, rate‑limit, logging). |
| **Service Mesh** | Istio | mTLS, traffic splitting for canary releases. |
| **Backend Services** | Go (high‑performance gRPC) & Python (FastAPI) | Go for latency‑critical video signaling; Python for LLM integration. |
| **LLM Inference** | vLLM (GPU‑accelerated) | Scalable, low‑latency generation of prescription narratives. |
| **Database** | PostgreSQL 15 + MongoDB 7 | Relational for audit‑ready data; document store for media. |
| **Search** | ElasticSearch 8 | Fast patient lookup, audit log query. |
| **Streaming** | Janus WebRTC + HLS fallback | Browser‑native, low‑latency, works on low‑bandwidth networks. |
| **Object Storage** | MinIO (S3‑compatible) | On‑premises encrypted storage, easy to swap to cloud S3. |
| **CI/CD** | GitHub Actions + ArgoCD | GitOps, automated roll‑backs. |
| **Observability** | OpenTelemetry → Grafana Loki + Prometheus | End‑to‑end tracing across mesh. |
| **Compliance** | OpenSCAP + AWS GuardDuty (if deployed on AWS) | Continuous security scanning. |

---  

## 7. Dependencies  

| Dependency | Version | License |
|------------|---------|---------|
| Kong | 3.5.0 | Apache‑2.0 |
| Istio | 1.22.0 | Apache‑2.0 |
| Go | 1.22 | BSD‑3 |
| Python | 3.11 | PSF |
| FastAPI | 0.110.0 | MIT |
| vLLM | 0.5.2 | Apache‑2.0 |
| Janus Gateway | 1.4.0 | GPL‑3 |
| Keycloak | 24.0.2 | Apache‑2.0 |
| PostgreSQL | 15.6 | PostgreSQL |
| MongoDB | 7.0 | SSPL |
| ElasticSearch | 8.13 | Elastic License (commercial) |
| MinIO | 2024‑10‑01T00‑00‑00Z | Apache‑2.0 |
| HAPI‑FHIR | 6.8.0 | Apache‑2.0 |

---  

## 8. Deployment Architecture  

### 8.1 Kubernetes Cluster  

* **Control Plane:** Managed (EKS / GKE) – version 1.30+.  
* **Node Pools:**  
  * `cpu‑pool` – 4 vCPU, 16 GiB – runs API Gateway, Auth, Integration Hub.  
  * `gpu‑pool` – 1 x NVIDIA A100, 64 GiB – runs vLLM inference pods.  
  * `media‑pool` – 8 vCPU, 32 GiB – runs Janus, Media Service, MinIO.  

All pods use **PodSecurityPolicy** “restricted”.  

### 8.2 Network  

* Ingress: **NGINX Ingress Controller** with TLS termination (Let’s Encrypt + internal PKI).  
* Service Mesh mTLS for east‑west traffic.  
* Egress via **AWS PrivateLink** (or Azure Private Endpoint) to external EMR APIs.  

### 8.3 Storage  

| Data | Storage | Encryption |
|------|---------|------------|
| Relational DB | Amazon RDS (PostgreSQL) | At‑rest AES‑256 |
| Document DB | Amazon DocumentDB (MongoDB compatible) | At‑rest AES‑256 |
| Media | MinIO on encrypted EBS volumes | Server‑side SSE‑AES256 |
| Logs/Traces | Loki (object storage backend) | TLS in‑flight, encrypted bucket |

### 8.4 CI/CD Flow  

1. **Push** → GitHub Actions runs unit tests, static analysis (golangci‑lint, bandit).  
2. **Docker Build** → Multi‑arch images pushed to ECR.  
3. **ArgoCD** detects new image tag → Canary rollout (5 % → 100 %).  
4. **Post‑deploy** health checks (probe endpoints).  
5. **Automated security scan** (Trivy) on each image; failures block promotion.  

---  

## 9. Security & Compliance  

| Area | Controls |
|------|----------|
| **Authentication** | OAuth2 + OpenID Connect via Keycloak; MFA enforced for providers. |
| **Authorization** | RBAC per role; fine‑grained policies stored in PostgreSQL `policy_rules`. |
| **Data Encryption** | TLS 1.3 everywhere; at‑rest AES‑256 for all storage. |
| **Audit Trail** | Immutable `audit_logs` table; write‑once via PostgreSQL `pg_logical`. |
| **HIPAA/GDPR** | Business Associate Agreement (BAA) template ready; data residency configurable (US/EU). |
| **Off‑Label Prescription** | Rule engine checks FDA‑approved indications; requires explicit patient consent flag stored in `prescriptions`. |
| **Incident Response** | Automated alerts via PagerDuty; forensic snapshots retained 30 days. |

---  

## 10. Scalability & Performance  

| Metric | Target | Test Method |
|--------|--------|-------------|
| **Concurrent Consultations** | 5,000 active video sessions | Load test with Locust + Janus stress scripts |
| **Prescription Generation Latency** | ≤ 800 ms (LLM inference) | vLLM benchmark on A100 |
| **API 99th‑percentile latency** | ≤ 150 ms (non‑media) | k6 load test |
| **Media Storage Throughput** | 10 Gbps aggregate ingest | MinIO benchmark suite |
| **Failover** | Zero‑downtime rolling upgrade | Istio canary + ArgoCD health checks |

Horizontal pod autoscaling (HPA) based on CPU, request latency, and custom Prometheus metrics (e.g., active video streams).  

---  

## 11. Monitoring & Observability  

* **Metrics:** Prometheus + Grafana dashboards (API latency, error rates, GPU utilization).  
* **Tracing:** OpenTelemetry (Jaeger UI) across all services.  
* **Logging:** Loki aggregation; alerts on `audit_logs` for privileged actions.  
* **Health Checks:** `/healthz` (liveness), `/readyz` (readiness) on each pod.  

---  

## 12. Risks & Mitigations  

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Regulatory change on off‑label prescribing** | Product may become non‑compliant | Modular rule engine; ability to toggle off‑label flag per jurisdiction. |
| **Low‑bandwidth rural connectivity** | Video quality degradation | Adaptive bitrate streaming; HLS fallback; audio‑only mode. |
| **LLM hallucination in prescription text** | Legal liability | Post‑generation validation step using deterministic rule engine; provider must approve before signing. |
| **Data breach** | HIPAA fines, reputation loss | End‑to‑end encryption, regular penetration testing, zero‑trust network. |
| **Vendor lock‑in (cloud storage)** | Migration cost | Use S3‑compatible MinIO; abstract storage via interface layer. |

---  

## 13. Release Plan  

| Milestone | Scope | Duration |
|-----------|-------|----------|
| **M0 – Foundations** | Infra (K8s, CI/CD), Auth Service, basic patient/provider CRUD | 4 weeks |
| **M1 – Consultation Core** | Video signaling, scheduling, media storage, basic UI | 6 weeks |
| **M2 – Prescription Engine** | vLLM integration, rule engine, PDF generation, e‑sign workflow | 5 weeks |
| **M3 – EMR Integration** | FHIR/HL7 adapters, bidirectional sync, pilot with one partner | 4 weeks |
| **M4 – Compliance Hardening** | Auditing, BAA, GDPR data‑subject tools, security audit | 3 weeks |
| **M5 – Beta Launch** | End‑to‑end flow with 2 rural clinics, collect usage & willingness‑to‑pay data | 4 weeks |
| **M6 – GA** | Full feature set, multi‑region deployment, SLA 99.9 % | 2 weeks |

---  

## 14. Glossary  

* **Off‑label therapy** – Use of a medical product outside its FDA‑approved indication.  
* **FHIR** – Fast Healthcare Interoperability Resources, a standard for exchanging healthcare information electronically.  
* **vLLM** – High‑throughput LLM inference engine (GPU‑optimized).  
* **Janus** – Open‑source WebRTC server.  

---  

*Prepared by the Rural‑Ortho‑Link Engineering Lead – AxentX*
