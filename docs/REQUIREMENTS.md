# Requirements.md
**Project:** rural-ortho-link  
**Owner:** AxentX – Telemedicine Product Team  
**Date:** 2026‑06‑16  
**Version:** 1.0  

---  

## 1. Overview  

rural‑ortho‑link is a secure, cloud‑native telemedicine platform that connects patients in underserved rural areas with board‑certified orthopedic specialists. The system enables:

* Video‑based consultations and asynchronous messaging.  
* Remote diagnostic data exchange (imaging, labs, wearable sensor streams).  
* Generation, review, and electronic transmission of off‑label therapy prescriptions that comply with FDA/EMA regulations.  

The platform must be production‑ready, scalable to **≥ 200 k concurrent users**, and integrate with existing AxentX infrastructure (vLLM for AI‑assisted triage, SGLang for structured note generation, and the shared BRAIN vector store).

---  

## 2. Functional Requirements  

| ID | Description | Priority |
|----|-------------|----------|
| **FR‑1** | **User Registration & Authentication** – Patients, clinicians, and admin staff must be able to create accounts, verify email/phone, and log in using OAuth2 (Google, Apple) or SSO (SAML) for enterprise clinicians. | High |
| **FR‑2** | **Role‑Based Access Control (RBAC)** – Enforce least‑privilege permissions: Patient, Orthopedic Specialist, Primary Care Provider, Pharmacy, System Admin. | High |
| **FR‑3** | **Appointment Scheduling** – Patients can view specialist availability, request slots, and receive confirmation/cancellation notifications via email/SMS. | High |
| **FR‑4** | **Live Video Consultation** – Browser‑based WebRTC session with adaptive bitrate, end‑to‑end encryption, and optional screen‑share for imaging review. | High |
| **FR‑5** | **Asynchronous Messaging** – Secure chat (text, image, PDF) with read receipts, searchable history, and AI‑generated summary notes (via vLLM). | Medium |
| **FR‑6** | **Diagnostic Data Upload** – Patients/PCPs can upload DICOM images, CSV sensor data, or PDFs; system stores files in encrypted object storage and indexes metadata in the BRAIN vector DB for similarity search. | High |
| **FR‑7** | **AI‑Assisted Triage** – Upon data upload, invoke vLLM to produce a preliminary risk score and suggested specialty, displayed to the triage nurse. | Medium |
| **FR‑8** | **Structured Clinical Documentation** – Use SGLang to generate SOAP notes, treatment plans, and discharge summaries in HL7‑FHIR format. | Medium |
| **FR‑9** | **Off‑Label Prescription Engine** – Clinician can create a prescription for off‑label therapy, attach justification, and trigger an automated compliance check (FDA/EMA). | High |
| **FR‑10** | **Electronic Prescription Transmission** – Send validated prescriptions to partnered pharmacies via e‑prescribing standards (NCPDP SCRIPT). | High |
| **FR‑11** | **Billing & Insurance Integration** – Capture CPT codes, generate claim payloads, and interface with major rural payer APIs. | Medium |
| **FR‑12** | **Audit Trail & Reporting** – Immutable log of all clinical actions, data accesses, and prescription events; exportable reports for compliance audits. | High |
| **FR‑13** | **Multilingual UI** – Support English and Spanish (initial launch) with locale‑aware date/number formatting. | Low |
| **FR‑14** | **Push Notifications** – Real‑time alerts for upcoming appointments, prescription status changes, and critical lab results. | Medium |
| **FR‑15** | **Admin Dashboard** – System health metrics, user management, role assignment, and data retention policy configuration. | High |

---  

## 3. Non‑Functional Requirements  

| ID | Requirement | Target |
|----|-------------|--------|
| **NFR‑1** | **Performance – Latency** – Video session setup < 2 s, end‑to‑end video latency ≤ 150 ms under normal broadband (5 Mbps downstream). | 95 % of sessions |
| **NFR‑2** | **Scalability** – Horizontal scaling to support 200 k concurrent users, 10 k simultaneous video streams. Auto‑scale based on CPU/Network metrics. | Kubernetes (EKS/GKE) |
| **NFR‑3** | **Availability** – 99.95 % uptime (≤ 4.38 h downtime/month) with multi‑region active‑active deployment. | SLA |
| **NFR‑4** | **Security – Data Protection** – All PHI encrypted at rest (AES‑256) and in transit (TLS 1.3). End‑to‑end encryption for video. | HIPAA compliant |
| **NFR‑5** | **Authentication** – MFA required for clinicians and admins. Passwords stored with Argon2id. | OWASP ASVS L2 |
| **NFR‑6** | **Compliance** – System must generate audit logs meeting 21 CFR 11 and GDPR (where applicable). | Immutable append‑only log |
| **NFR‑7** | **Reliability** – Automatic failover within 30 s; data replication factor ≥ 3 across zones. | Disaster Recovery |
| **NFR‑8** | **Observability** – Centralized logging (ELK), metrics (Prometheus + Grafana), tracing (OpenTelemetry). | Alert thresholds defined |
| **NFR‑9** | **Maintainability** – Codebase follows AxentX Python/Node style guide; 80 % unit test coverage; CI/CD pipeline with automated security scans. | CI/CD |
| **NFR‑10** | **Data Retention** – Clinical records retained 10 years; logs retained 1 year; configurable per jurisdiction. | Configurable policy |
| **NFR‑11** | **Usability** – Average task completion time ≤ 3 min for appointment booking; UI passes AA‑100 accessibility score. | User testing |
| **NFR‑12** | **Internationalization** – Unicode‑compliant; locale files externalized. | i18n ready |
| **NFR‑13** | **Resource Efficiency** – Video transcoding cost ≤ $0.001 per minute per stream. | Cost target |

---  

## 4. Constraints  

1. **Technology Stack** – Must use existing AxentX components:  
   * Backend: Python 3.11, FastAPI, PostgreSQL (Citus for sharding).  
   * AI services: vLLM (inference) and SGLang (structured generation) accessed via internal gRPC.  
   * Vector store: Shared BRAIN (pgvector) for similarity search.  

2. **Regulatory** – All prescription workflows must pass the internal **Off‑Label Compliance Service** (already deployed).  

3. **Deployment** – Must run on AxentX‑approved Kubernetes clusters (EKS‑prod‑us‑east‑1, GKE‑prod‑europe‑west1).  

4. **Data Residency** – PHI of EU patients must remain within EU region; US data must stay in US regions.  

5. **Budget** – Monthly cloud spend for the MVP must not exceed **$120k**.  

---  

## 5. Assumptions  

| ID | Assumption |
|----|------------|
| **A‑1** | Rural broadband availability averages ≥ 5 Mbps downstream; fallback to audio‑only mode is acceptable. |
| **A‑2** | Orthopedic specialists will adopt the platform voluntarily after a 2‑week onboarding program. |
| **A‑3** | Partner pharmacies support NCPDP SCRIPT v20180701 for e‑prescribing. |
| **A‑4** | Existing AxentX AI models (vLLM) are sufficiently trained on orthopedic triage data; fine‑tuning will be performed in‑house. |
| **A‑5** | Legal team has approved the off‑label prescription workflow template. |
| **A‑6** | The shared BRAIN vector store can handle an additional 5 M new embeddings per month without performance degradation. |
| **A‑7** | Users will access the platform via modern browsers (Chrome ≥ 108, Edge ≥ 108, Safari ≥ 15). |
| **A‑8** | No offline (store‑and‑forward) mode is required for the MVP; connectivity is assumed for all interactions. |

---  

## 6. Acceptance Criteria  

* All **FR‑1 – FR‑15** are implemented and pass automated integration tests.  
* Performance tests meet **NFR‑1** and **NFR‑2** thresholds.  
* Security audit (SOC 2 Type II) passes with no critical findings.  
* Successful end‑to‑end prescription flow validated with a pilot pharmacy.  
* Deployment to production with zero‑downtime migration from the current prototype.  

---  

*Prepared by:* Senior Product/Engineering Lead – AxentX  
*Reviewed by:* Architecture Review Board, Compliance, Security, QA  

---
