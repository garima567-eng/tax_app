# 🛡️ TaxRefund-Guard: Machine Learning Audit Triage Platform

An AI-driven risk-triage engine designed to protect public revenue by intercepting anomalous Value-Added Tax (VAT) and Goods and Services Tax (GST) refund claims. Built on a hybrid architecture combining supervised ensemble learning with explainable AI (XAI) frameworks, the platform bridges the gap between machine learning probabilities and statutory tax compliance workflows.

---

## 🎯 The Core Business Problem
State excise and taxation departments manually audit only 1–2% of all refund applications annually due to resource constraints. Sophisticated tax evasion schemes—such as carousels or phantom invoice manufacturing—exploit this bottleneck by submitting fraudulent credit refunds that look compliant on paper. This platform solves the challenge by shifting tax administration from **reactive sampling** to **predictive triage**.

## 🚀 Key Architectural Features

* **Dual-Channel Ingestion Stream:** Seamlessly switches between a single manual application evaluation dashboard and an asynchronous batch-file processor capable of scoring whole daily registries (`.csv`).
* **Explainable AI (XAI Integration):** Incorporates dynamic global feature importance metrics extracted directly from the random forest estimators, providing auditors with transparent, defensible rationales for why an application was flagged.
* **Deterministic Policy Enforcement Gateways:** Uses programmatic boundaries to transform decimal risk values into high-impact color-coded administrative directives:
  * **Auto-Approve (<30% Prob.):** Clears compliant claims instantly to preserve business cash-flow velocity.
  * **Desk Review (30%–75% Prob.):** Flags moderate variances, prompting localized document checks.
  * **Audit Hold (>75% Prob.):** Immediately freezes treasury outlays and alerts field enforcement units.

---

## 📊 Pipeline Layout & Data Topology
[ Raw Transactional Data Input: Invoices, Filings, Vendor IDs ]
│
▼
[ Feature Engineering Engine: Normalizing Scale via Financial Ratios ]
- Claim-to-Turnover Metric
- Supplier Compliance Footprint Matrix
- Filing Latency Windows
│
▼
[ Random Forest Classifier (Balanced Weights Configuration) ]
│
▼
┌────────────────────┴────────────────────┐
▼                                         ▼
[ Prediction: Fraud Probability % ]      [ Global Feature Weight Logs ]
│                                         │
▼                                         ▼
[ Policy Triage Logic Gateway ]             [ Interactive XAI Charts ]

Green: Fast-Track Disbursal

Orange: Manual Desk Verification

Red: System Freeze & Field Raid

---
---

## 🛠️ Tech Stack & Foundations
* **Modeling Backend:** Python 3, `scikit-learn`, `pandas`, `numpy`.
* **Visualization Suite:** `matplotlib`, `seaborn` for macro clustering distributions.
* **Frontend Interface UI:** Streamlit UI Architecture with inline HTML/CSS semantic injection wrappers.
* **Algorithm Blueprint:** **Random Forest Classifier** configured with `class_weight='balanced'` to explicitly counter extreme target data imbalances (where fraud outliers naturally make up only ~3% of actual filings).

---

## 💾 Local Installation & Deployment

### 1. Clone the Repository Workspace
```bash
git clone [https://github.com/garima567-eng/tax_app.git](https://github.com/garima567-eng/tax_app.git)
cd tax_app.
