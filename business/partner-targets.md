**partner-targets.md**  
*Tele‑medicine platform **rural‑ortho‑link** – partner integration roadmap*  

| # | SaaS / API | Core Capability | Free‑Tier Limits* | Integration Effort | Value‑Add (User Job) | Affiliate / Rev‑Share Potential | Priority |
|---|------------|----------------|-------------------|--------------------|----------------------|--------------------------------|----------|
| 1 | **Twilio Programmable Video** | Secure, low‑latency video calls (HIPAA‑enabled) | 1 M min/month, 100 GB recording | **M** – SDK embed, token server, compliance config | “Connect with a specialist” – real‑time consult | 20 % of per‑call revenue (standard Twilio partner) | ★★★★★ |
| 2 | **Luma Health (Patient Engagement API)** | Automated appointment reminders, two‑way SMS, intake forms | 200 messages/mo, 5 templates | **S** – webhook registration, simple REST calls | “Schedule & prepare for consult” – reduces no‑shows | Referral fee $0.10 per confirmed appointment | ★★★★ |
| 3 | **Redox (EHR Integration Hub)** | Bi‑directional data exchange with major EHRs (Epic, Cerner) | 5 connections, 10 k records/mo | **L** – mapping FHIR resources, OAuth flows | “Share imaging & prior notes” – gives specialist full context | Revenue‑share on each successful claim submission (≈5 % of claim value) | ★★★ |
| 4 | **PillPack / Amazon Pharmacy API** | Prescription fulfillment, medication shipping to rural addresses | 50 prescriptions/mo (sandbox) | **M** – order creation, status callbacks | “Get off‑label therapy delivered” – closes the care loop | 3 % of prescription value for each fulfilled order | ★★★★ |
| 5 | **Google Cloud Healthcare API (FHIR Store)** | Centralised, standards‑based storage of imaging (X‑ray, MRI) | 1 TB storage, 100 k reads/mo | **M** – FHIR resource upload, IAM setup | “View diagnostic images during consult” – improves diagnosis | No direct rev‑share, but qualifies for Google Cloud partner credits | ★★ |
| 6 | **Clearbit Enrichment API** | Auto‑populate patient demographic & insurance data from email/phone | 50 lookups/mo | **S** – simple REST call, caching layer | “Pre‑fill intake forms, verify coverage” – speeds onboarding | Affiliate payout $0.05 per enriched record | ★★ |
| 7 | **Stripe Connect (Custom Accounts)** | Payments, co‑pay collection, revenue split with providers | $0 setup, 2 % per‑transaction fee (standard) | **M** – OAuth onboarding, webhook handling | “Collect co‑pay & enable provider payouts” – monetises platform | 10 % of platform fee (standard Stripe partner) | ★★★★★ |
| 8 | **Klarna / Afterpay API** | Buy‑now‑pay‑later for expensive orthotic devices | $0 setup, 3 % per‑transaction fee | **S** – checkout integration, risk webhook | “Make costly devices affordable” – expands adoption | Affiliate commission 1 % of financed amount | ★★★ |

\*Free‑tier limits are as of 2024‑12‑01; they are sufficient for MVP testing (≤ 2 k active users).  

---

### Integration Roadmap (Quarterly)

| Quarter | Milestones | Target Partners (by priority) | Success Metrics |
|---------|------------|------------------------------|-----------------|
| **Q1 – Foundations** | • Core video & scheduling stack <br>• HIPAA compliance audit | 1️⃣ Twilio Video <br>2️⃣ Luma Health <br>7️⃣ Stripe Connect | • 100 % video call success rate <br>• ≤ 5 % no‑show rate <br>• 80 % of consults billed |
| **Q2 – Clinical Data Exchange** | • Secure imaging upload & view <br>• Basic EHR sync for referral notes | 5️⃣ Google Cloud Healthcare <br>3️⃣ Redox (pilot with one EHR) | • 90 % of images load <br>• 1 EHR integration live (≥ 10 referrals) |
| **Q3 – Prescription & Fulfilment** | • Prescription order flow <br>• Automated shipping notifications | 4️⃣ PillPack / Amazon Pharmacy <br>6️⃣ Clearbit (enrichment) | • 80 % of prescriptions fulfilled within 48 h <br>• 95 % data completeness on intake |
| **Q4 – Payment Flexibility & Scaling** | • BNPL checkout <br>• Revenue‑share reporting dashboard | 8️⃣ Klarna / Afterpay <br>7️⃣ Stripe Connect (full payout) | • 30 % of device purchases use BNPL <br>• 10 % YoY revenue uplift from affiliate streams |
| **Post‑Launch (Year 2)** | • Expand Redox to additional EHRs <br>• Negotiate higher‑tier rev‑share with Twilio & Stripe | 3️⃣ Redox (scale) <br>1️⃣ Twilio (enterprise tier) | • 5 EHR partners <br>• 20 % reduction in per‑call cost via volume discounts |

---

### Why These Partners?

* **Revenue‑share focus:** Twilio, Stripe, Redox, PillPack, Klarna all offer affiliate or transaction‑based payouts, directly feeding the **“monetise rural orthopedics”** KPI.  
* **Free‑tier bootstrap:** Enables us to launch an MVP with ≤ $2 k cloud spend while validating demand.  
* **Job‑to‑be‑done alignment:** Each integration closes a specific step in the patient journey—**connect**, **prepare**, **inform**, **prescribe**, **pay**, **receive**—ensuring a frictionless end‑to‑end experience.  
* **Scalable compliance:** Twilio Video and Redox are already HIPAA‑ready, reducing legal overhead.  

---  

*Prepared by Business‑Synthesis, Axentx OS – 2026‑06‑16*