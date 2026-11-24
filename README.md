# KisanSAATHI 2.0 – Smart Agricultural Intelligence Ecosystem
> **Tagline:** Your Digital Krishi Officer  
> **Category:** AgriTech | Artificial Intelligence | Machine Learning | Market Intelligence | Web3 | Digital Agriculture  
> **Architecture:** Strict Python-First, Zero-Node.js, Production-Oriented Django SaaS  

[![Django](https://img.shields.io/badge/Django-6.1-forestgreen.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.14-red.svg)](https://pytorch.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-5.0-green.svg)](https://opencv.org/)
[![Tests](https://img.shields.io/badge/Tests-13%20Passed-brightgreen.svg)]()
[![Web3](https://img.shields.io/badge/Web3-SHA256%20%7C%20EVM-purple.svg)]()

---

## 🌾 1. Overview & Vision

**KisanSAATHI 2.0** is an enterprise-grade, accessible, and multilingual agricultural intelligence platform engineered to empower Indian farmers, FPOs (Farmer Producer Organizations), verified institutional buyers, and agricultural administrators.

Unlike informational websites with static dashboards or mock buttons, **KisanSAATHI 2.0** is a full-stack, data-driven decision-support system. It computes actual net revenue after real logistical costs, performs non-hallucinatory AI consultations, audits crop health using computer vision preprocessing, verifies transactions via cryptographic SHA-256 receipt ledgers anchored to Ethereum smart contracts, and ensures full accessibility across rural environments.

### Strict Python-First Engineering Mandate
- **No Node.js, npm, npx, React, Next.js, Vite, or Webpack.**
- Entirely powered by **Python 3.12+**, **Django 6.1**, **Django ORM**, **PyTorch**, **OpenCV**, **ReportLab**, and modern semantic **HTML5/CSS3** with minimal vanilla JavaScript.
- Direct server-rendered templates ensuring lightning-fast load times on 2G/3G/4G rural mobile connections.

---

## 🚀 2. Core Pillars & Architecture

```
                               ┌────────────────────────────────────────────────────────┐
                               │                    KISANSAATHI 2.0                     │
                               │               Your Digital Krishi Officer              │
                               └──────────────────────────┬─────────────────────────────┘
                                                          │
          ┌───────────────────────┬───────────────────────┼───────────────────────┬───────────────────────┐
          ▼                       ▼                       ▼                       ▼                       ▼
 ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
 │  Smart Mandi &  │     │   AI Krishi     │     │ Net Realisation │     │ Web3 Blockchain │     │  Farmer & FPO   │
 │   Market Data   │     │  Intelligence   │     │   Calculator    │     │  Trust Ledger   │     │ Buyer Network   │
 └────────┬────────┘     └────────┬────────┘     └────────┬────────┘     └────────┬────────┘     └────────┬────────┘
          │                       │                       │                       │                       │
 • Agmarknet/OGD          • OpenCV Blur Variance  • Gross vs Deductions   • Canonical JSON Hashing• 4-Tier Verification
 • Modal, Min, Max Price  • PyTorch Inference     • APMC Cess & Haulage   • SHA-256 Digest        • Collective Pooling
 • Arrivals & Distance    • Univ. Chem Dosages    • Dynamic Optimal Route • Sepolia EVM Anchor    • Direct Procurement
 • Cross-Mandi Compare    • Strict Safety Notice  • ReportLab PDF Export  • Tamper Detection Alert• Escrow Reconciliation
```

### 1. Smart Mandi & Market Intelligence (`apps.markets`)
- Real-time price tracking across APMC mandis (Modal, Min, Max prices, and Arrivals in Quintals).
- Dual tagging: Verified official records vs Agmarknet/OGD demo feeds.
- Inter-mandi comparison tool allowing farmers to compare price variances across neighboring districts.

### 2. Net Realisation & Crop Selling Calculator (`apps.calculator`)
- Solves the critical farmer pitfall: *higher headline mandi price does not equal higher profit*.
- Deducts distance-based freight, loading/unloading labor, APMC market cess, bagging/packaging costs, and moisture/quality deductions.
- Automatically ranks options by net pocket revenue and exports **branded ReportLab PDF audit reports**.

### 3. AI Crop Wellness & Screening Center (`apps.crop_wellness`)
- **OpenCV Blur Detection:** Uses Laplacian variance (`cv2.Laplacian`) to reject blurry field photos before wasting computation.
- **PyTorch Neural Feature Extractor:** Multi-scale feature extraction combined with confidence calibration.
- **Actionable Agronomy:** Delivers exact ICAR/State University recommended pesticide/fungicide chemical dosages (e.g., *Hexaconazole 5% EC @ 2ml/L*).
- **Mandatory Safety Disclaimer:** Clearly distinguishes AI decision-support from certified laboratory pathology.

### 4. Grounded AI Krishi Officer (`apps.assistant`)
- Non-hallucinatory voice & text agricultural conversational assistant.
- Multilingual support: **Hindi (हिन्दी)**, **English**, **Punjabi (ਪੰਜਾਬੀ)**, and **Haryanvi (हरियाणवी)**.
- Strictly grounds price queries and scheme information to real database rows; provides instant disclaimers if unverified queries are made.

### 5. Government Scheme Discovery & Eligibility Wizard (`apps.schemes`)
- Curated repository of Central and State schemes (PM-KISAN, PMFBY Crop Insurance, Soil Health Card, PM Krishi Sinchayee Yojana, Agri Infrastructure Fund).
- Interactive 3-step eligibility wizard evaluating land size, category, crop type, and Aadhaar linkage.
- Direct links to official government application portals.

### 6. Verified Buyer & FPO Aggregation Network (`apps.buyers`, `apps.fpos`)
- **4-Level Buyer Verification:** Basic, GSTIN-verified, FSSAI-licensed, and Bank-guaranteed.
- Direct farmer enquiries and quote submission.
- FPO collective pooling allows smallholder farmers to aggregate produce to meet bulk industrial procurement orders.

### 7. Web3 Trust Ledger & Tamper Detection (`apps.web3_ledger`)
- Generates canonical JSON digital receipts containing unique serial numbers, parties, quantities, and net amounts.
- Hashes data into a cryptographically immutable **SHA-256 fingerprint** anchored to the `AgriTrustLedger.sol` Ethereum smart contract on Sepolia.
- Real-time tamper detection: changing even a single rupee in transaction parameters instantly alerts the verifier with mismatch proofs.

### 8. Inclusive Accessibility Architecture (`apps.accessibility`, `apps.multilingual`)
- **Theme Modes:** Light, Dark, High-Contrast (Black & Yellow for low-vision rural users), and Large/Jumbo Text Scaling.
- **Simple Farmer Mode:** Replaces complex tables with oversized, single-tap visual action tiles.
- **Web Speech API:** Built-in microphone voice inputs and read-aloud synthesizers.

---

## 🛠️ 3. Quick Start & Local Setup

### Prerequisites
- Python 3.12+ (accessible via `python` or `py`)
- Git

### Step-by-Step Installation

```bash
# 1. Clone the repository and enter directory
cd "d:\geeta university"

# 2. Install all Python dependencies (Zero Node.js required)
py -m pip install -r requirements.txt

# 3. Apply database migrations
py manage.py migrate

# 4. Seed realistic demonstration data
py scripts/seed_demo_data.py

# 5. Launch the development server
py manage.py runserver
```

Open your browser at: **`http://127.0.0.1:8000/`**

---

## 👥 4. Pre-Seeded Demonstration Accounts

All accounts come pre-loaded with realistic crops, transactions, orders, and receipts.

| Role | Username | Password | Context / Persona |
|---|---|---|---|
| **Farmer (Haryana)** | `ramesh_karnal` | `farmer123` | 5.5 Acre Wheat & Mustard farmer in Karnal. Has active crops and anchored receipts. |
| **Farmer (Punjab)** | `gurpreet_pb` | `farmer123` | 12 Acre Basmati Rice farmer in Ludhiana. Active FPO member. |
| **Verified Buyer** | `shiva_agro` | `buyer123` | Level-3 Verified Agro Processor looking for 500 MT Sharbati Wheat. |
| **FPO Admin** | `fpo_samriddhi` | `fpo123` | Admin of Samriddhi Kisan Producer Co. with 240+ members & collective pools. |
| **Platform Admin** | `admin` | `admin123` | Master administrator overseeing users, audits, schemes, and verification. |

---

## 🧪 5. Automated Verification & Testing

KisanSAATHI 2.0 includes an automated test suite covering all security, calculation, AI, accessibility, and blockchain modules:

```bash
# Run the complete test suite
py -m pytest
```

### Verified Test Cases (13 Passed):
1. `test_farmer_registration`: Role assignment, default preferences, and secure profile creation.
2. `test_user_login_and_logout`: Authentication lifecycle and dashboard redirection.
3. `test_calculator_math_and_ranking`: Net realisation formula correctness and profit-maximizing mandi sorting.
4. `test_pdf_report_export`: ReportLab programmatic PDF generation and byte-stream delivery.
5. `test_mandi_price_filtering`: Search and district-level price filtering.
6. `test_disease_profile_and_safety_disclaimer`: Pathogen profile accuracy and university dosage rendering.
7. `test_scheme_directory_and_eligibility`: Wizard logic for PM-KISAN and PMFBY.
8. `test_grounded_price_and_scheme_responses`: Non-hallucinatory AI Assistant query engine.
9. `test_buyer_requirement_and_fpo_membership`: Enterprise buyer workflow and FPO pool participation.
10. `test_canonical_hash_and_tamper_detection`: Cryptographic verification and mismatch alerts.
11. `test_receipt_verification_workflow`: Public verification view with valid transaction records.
12. `test_language_switch`: Multilingual session translation middleware.
13. `test_accessibility_toggle`: High-contrast, dark mode, and font-scale persistence.

---

## 🔗 6. Web3 Trust Ledger & Tamper Demonstration

To demonstrate tamper-proof transparency during evaluations or hackathon presentations:

1. Navigate to: `http://127.0.0.1:8000/ledger/verify/?code=KS-REC-2026-X0001`
   - **Result:** Green badge, valid cryptographic fingerprint matching contract record `0xd855e626a0be...`.
2. Navigate to: `http://127.0.0.1:8000/ledger/verify/?code=KS-REC-2026-X0001&tamper=1`
   - **Result:** Red critical security alert, displaying exact hash mismatch and warning of illicit offline tampering.

### Smart Contract Deployment
The Solidity contract is located at `blockchain/contracts/AgriTrustLedger.sol` and can be compiled and deployed using standard Foundry or Remix tools:
```solidity
contract AgriTrustLedger {
    struct ReceiptRecord {
        bytes32 receiptHash;
        uint256 timestamp;
        address recorder;
        bool isRevoked;
    }
    // ...
}
```

---

## 📂 7. Project Directory Layout

```
d:\geeta university/
├── apps/
│   ├── accounts/          # Custom User model (FARMER, BUYER, FPO_ADMIN, ADMIN) & AuditLog
│   ├── farmers/           # FarmerProfile & FarmerCrop lifecycle tracking
│   ├── buyers/            # BuyerProfile (4 verification tiers) & BuyerRequirements
│   ├── fpos/              # FPO management, collective crop lot aggregation & pools
│   ├── crops/             # Crop taxonomy & Government MSP benchmarks
│   ├── markets/           # APMC Mandi master, daily prices & cross-mandi comparator
│   ├── calculator/        # Net Realisation Calculator & ReportLab PDF generator
│   ├── crop_wellness/     # OpenCV blur detection, PyTorch inference & disease profiles
│   ├── schemes/           # Central/State scheme discovery & 3-step eligibility wizard
│   ├── assistant/         # Grounded AI Krishi Officer engine (EN, HI, PA, HR)
│   ├── logistics/         # WDRA-accredited storage facilities & rural transporters
│   ├── transactions/      # Sale contracts, fee breakdown & settlement records
│   ├── web3_ledger/       # Canonical JSON SHA-256 hashing & EVM anchoring service
│   ├── accessibility/     # High-contrast, font scaling & simple farmer mode engine
│   ├── multilingual/      # Translation dictionaries & language switching middleware
│   ├── notifications/     # Event-driven price, scheme & buyer alerts
│   └── dashboard/         # Role-based dispatchers & public marketing views
├── blockchain/
│   └── contracts/         # AgriTrustLedger.sol Ethereum smart contract
├── config/                # Django core settings, middleware pipeline & root URLs
├── scripts/
│   └── seed_demo_data.py  # Comprehensive database seeder with realistic agro data
├── static/
│   ├── css/style.css      # Agricultural green design system, high-contrast & themes
│   └── js/main.js         # Vanilla JS mobile drawer, voice recognition & widgets
├── templates/             # 28+ clean server-rendered Django templates
├── tests/
│   └── test_platform.py   # Full 13-test automated pytest suite
├── .env.example           # Environment configuration blueprint
├── manage.py              # Django management binary
├── pytest.ini             # Pytest test-runner configuration
└── requirements.txt       # Production Python dependencies
```

---

## 🔒 8. Security & Data Integrity

- **Backend Role Enforcement:** Sensitive actions (approving buyers, creating FPO pools, editing crop records) are protected via Django `@login_required` and custom role-based view guards.
- **No PII on Blockchain:** Only canonical SHA-256 digests and serial identifiers are committed to the public ledger; farmer identities remain private.
- **CSRF & Password Hashing:** Powered by Django's PBKDF2 password hasher with SHA-256 iterations and global CSRF token verification on all POST forms.
- **Calibrated AI Outputs:** AI disease screening reports include explicit confidence levels and recommend laboratory confirmation before spraying critical chemicals.

---

## 📄 9. License & Credits

Built with pride for Indian Farmers and Agricultural Communities.  
**KisanSAATHI 2.0** — *Your Digital Krishi Officer*.
