```markdown
# dataflow.md

## System Dataflow Architecture

### ASCII Block Diagram

```
+-------------------+     +-------------------+     +------------------------+
|                   |     |                   |     |                        |
|  External Sources +----->  Ingestion Layer  +----->  Processing/Transform  |
|                   |     |                   |     |         Layer          |
+-------------------+     +--------+----------+     +-----------+------------+
                                   |                            |
                                   v                            v
+-------------------+     +--------+----------+     +-----------+------------+
|                   |     |                   |     |                        |
|   Auth Boundary   |<----+   Storage Tier    +<----+                        |
|   (IAM, RBAC)     |     |                   |     |                        |
+-------------------+     +--------+----------+     +-----------+------------+
                                   |                            |
                                   v                            v
                         +---------+----------+     +-----------+------------+
                         |                    |     |                        |
                         |  Query/Serving     +----->   Egress to User       |
                         |      Layer         |     |                        |
                         +--------------------+     +------------------------+
```

> **Legend**:  
> → Data flow  
> ←→ Auth & policy enforcement (OAuth2, JWT, RBAC)  
> All layers enforce zero-trust via IAM and attribute-based access control (ABAC) at microservice edges.

---

### External Data Sources

- **EMR Systems (via FHIR APIs)**  
  - Epic, Cerner (HL7/FHIR R4 endpoints)  
  - Data: Patient demographics, medical history, imaging metadata  
  - Auth: SMART on FHIR with OAuth2.0, patient consent scopes

- **Rural Clinic EHR Feeds (CSV/HL7 over SFTP)**  
  - Batch uploads from partner clinics  
  - Frequency: Daily at 02:00 UTC  
  - Format: HL7 v2.x or structured CSV with PHI de-identified at source

- **Specialist Network (gRPC API)**  
  - Orthopedic specialists registered in platform  
  - Real-time availability, credentialing status, specialty tags (e.g., spine, trauma)

- **Pharmacy Partners (REST API)**  
  - For off-label prescription fulfillment tracking  
  - Endpoints: `/prescription/status`, `/formulary/check`

- **Patient Mobile App (HTTPS/WebSocket)**  
  - Symptom logs, photo uploads (wound tracking), appointment feedback  
  - Auth: OIDC + biometric device binding

---

### Ingestion Layer

- **Apache Kafka (Cluster: `ingest-kafka-01`)**  
  - Topics: `patient_events`, `eoc_clinics`, `specialist_updates`, `rx_requests`  
  - Retention: 7 days (compact + delete)  
  - Throughput: ~1.2K msg/sec peak

- **Kafka Connectors**  
  - FHIR → Kafka: Custom connector using HAPI FHIR  
  - SFTP Poller: Airbyte-based ingestion pipeline (schedule: daily)  
  - gRPC Source: Envoy proxy to bridge gRPC to Kafka (Protobuf over HTTP/2)

- **API Gateway (Kong 3.8 + OpenID Connect)**  
  - Rate-limited endpoints for mobile/web clients  
  - JWT validation at edge; scopes: `patient`, `provider`, `admin`

- **Auth Boundary**  
  - All ingress points require mTLS or OIDC  
  - PHI data tagged with `sensitivity=L4` at entry

---

### Processing/Transform Layer

- **Apache Flink (Stateful Stream Processing)**  
  - Jobs:  
    - `patient_journey_enricher`: Joins clinic data with specialist availability  
    - `offlabel_presc_detector`: Flags potential off-label Rx based on FDA/EMA labels + clinical guidelines  
    - `risk_stratifier`: Uses XGBoost model (v1.4) to predict mobility decline risk (AUC 0.87)  

- **Python Microservices (FastAPI, Dockerized)**  
  - `/transform/imaging_metadata`: Extracts DICOM tags → JSON-LD  
  - `/nlp/consult_notes`: Fine-tuned `biomed_roberta_base` for symptom extraction (F1=0.91)  

- **Data Quality Checks (Great Expectations)**  
  - Validates:  
    - 95% of patient records contain `referral_source`  
    - `specialist_response_time` < 48h SLA  
  - Alerts on drift via Prometheus + Grafana

- **Auth Boundary**  
  - Service-to-service auth via SPIFFE/SPIRE  
  - Model inference endpoints require `role=ml-infer` token

---

### Storage Tier

- **Primary DB: PostgreSQL 15 (RDS, Multi-AZ)**  
  - Schemas:  
    - `patients`, `encounters`, `prescriptions`, `specialist_roster`  
  - Encryption: TDE + row-level security (RLS)  
  - Backup: PITR enabled (RPO < 5 min)

- **Time-Series: TimescaleDB (on PG)**  
  - Tables: `vitals_log`, `pain_score_tracking`  
  - Chunk size: 24h intervals

- **Document Store: MongoDB Atlas (M20)**  
  - Collections: `consult_transcripts`, `imaging_reports`, `consent_forms`  
  - Indexes: `$text` on clinical notes; TTL on temp uploads

- **Cold Storage: S3 (HIPAA-compliant bucket)**  
  - Prefixes: `/dicom`, `/patient_videos`, `/audit_logs`  
  - Lifecycle: Glacier after 365 days

- **Auth Boundary**  
  - All DBs behind VPC; IAM roles restrict per-service access  
  - PHI access requires MFA + just-in-time (JIT) elevation via Hashicorp Vault

---

### Query/Serving Layer

- **GraphQL API (Apollo Server + Node.js)**  
  - Schema: Unified view across PG, MongoDB, and cache  
  - Resolvers:  
    - `patient(caseId: ID!)`: Aggregates from 4 sources  
    - `availableSpecialists(zip: String!)`: Geo-filtered + load-aware  

- **Read Replicas (PostgreSQL)**  
  - 3x read-only instances for analytics dashboards

- **Redis (ElastiCache, Cluster Mode)**  
  - Caches:  
    - Specialist availability (TTL: 60s)  
    - Formulary lookup results (TTL: 4h)  
  - Auth: Redis ACLs + TLS

- **Model Serving (Triton Inference Server on EKS)**  
  - Hosts:  
    - `risk_stratifier_v2` (PyTorch)  
    - `rx_safety_checker_v1` (ONNX)  
  - Autoscaling: 1 → 10 pods (based on 99th %ile latency < 350ms)

- **Auth Boundary**  
  - All queries require JWT + context-aware policies (e.g., a patient cannot query other patients)  
  - Audit trail: Every query logged to `audit_log_stream` (immutable)

---

### Egress to User

- **Web Portal (React + AppSync)**  
  - Role-based dashboards:  
    - Patient: Appointment scheduling, Rx tracking  
    - Specialist: Queue management, e-consult editor  
  - Data: Served via GraphQL subscriptions

- **Mobile App (React Native, HIPAA-compliant)**  
  - Features: Photo capture (wound healing), push for Rx status  
  - Sync: Offline-first with encrypted Realm DB

- **Email/SMS (Twilio + SES)**  
  - Templates:  
    - `rx_filled_alert` (SMS)  
    - `follow_up_scheduled` (Email)  
  - Opt-out compliance: One-click unsubscribe + audit

- **HL7v2 Outbound (Mirth Connect)**  
  - Pushes summary care records back to rural clinics  
  - Format: ORU^R01, ADT^A08

- **Auth Boundary**  
  - All egress filtered by data minimization policies  
  - PHI never sent via SMS; only notification tokens  
  - Patient consent required before any outbound data share (stored in `consent_db`)
```