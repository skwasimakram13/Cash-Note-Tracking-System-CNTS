# Cash Note Tracking System (CNTS)
> A Computer Vision–powered cash inflow & outflow control system for CSP / cash-intensive businesses

---

## 🧠 Problem Statement

Cash-based CSP operations suffer from:
- Manual reconciliation errors
- Employee-led note substitution or hiding
- Zero traceability at the **individual banknote level**
- End-of-day mismatches with no forensic proof

Traditional accounting tracks **amounts**.  
Fraud happens at the **note level**.

**CNTS solves this by digitizing every physical banknote.**

---

## 🎯 Objective

To build a desktop-based software that:
- Detects Indian currency denomination (₹50 / ₹100 / ₹200 / ₹500)
- Reads and stores **unique serial numbers** using camera + OCR
- Tracks **IN / OUT** movement of every note
- Maintains real-time drawer balance
- Prevents, detects, and audits cash theft

---

## 🏗️ System Architecture (High Level)

USB Camera
↓
Image Capture
↓
Note Detection (Denomination)
↓
Serial Number OCR
↓
Validation Layer
↓
Ledger Database
↓
Dashboard & Reports


This is a **Cash Digital Twin** architecture.

---

## 🖥️ Hardware Requirements

| Component | Minimum Spec |
|---------|--------------|
| Desktop OS | Windows 10 / 11 |
| Camera | USB HD Camera (1080p, fixed focus) |
| Mount | Fixed overhead mount (non-movable) |
| Lighting | White LED (diffused, shadow-free) |
| Desk Surface | Matte black base |

⚠️ **Camera angle and lighting must NEVER change**

---

## 🧰 Tech Stack

### Core
- **Python 3.10+**
- **OpenCV** – image processing
- **YOLOv8** – note denomination detection
- **Tesseract OCR** – serial number extraction

### Backend
- **SQLite / PostgreSQL**
- **SQLAlchemy ORM**

### Frontend (Desktop)
- **PyQt / Tkinter**
- Offline-first design

---

## 🧩 Key Features

### ✔ Denomination Detection
- Identifies ₹50 / ₹100 / ₹200 / ₹500 notes
- Confidence-based validation

### ✔ Serial Number OCR
- Crops serial number region
- Image enhancement before OCR
- Regex-based validation
- Confidence threshold enforcement

### ✔ Cash In / Cash Out Workflow
- Mandatory scan for every note
- No manual amount entry
- Real-time calculation

### ✔ Anti-Theft Controls
- Duplicate serial detection
- Withdraw-only-existing-notes rule
- Scan refusal on mismatch

### ✔ Audit & Reporting
- End-of-day reconciliation
- Operator-wise activity logs
- Missing note alerts

---

## 🔄 Operational Flow

### CASH IN (Deposit / Received Cash)

1. Operator selects **Cash In**
2. Places notes one by one under camera
3. System detects:
   - Denomination
   - Serial Number
4. Note stored as `IN`
5. Drawer balance updated automatically

### CASH OUT (Withdrawal)

1. Operator selects **Cash Out**
2. Required amount displayed
3. Notes must be scanned
4. System verifies note availability
5. Notes marked as `OUT`

🚫 No scan → No transaction

---

## 🗃️ Database Schema

### `notes`
| Column | Type | Description |
|------|------|------------|
| serial_number | TEXT (PK) | Unique note ID |
| denomination | INTEGER | 50 / 100 / 200 / 500 |
| status | TEXT | IN / OUT |
| last_seen | TIMESTAMP | Last scan time |

### `transactions`
| Column | Type |
|------|------|
| id | INTEGER (PK) |
| type | IN / OUT |
| total_amount | INTEGER |
| operator_id | INTEGER |
| timestamp | TIMESTAMP |

### `operators`
| Column | Type |
|------|------|
| id | INTEGER |
| name | TEXT |
| login_id | TEXT |

---

## 🛡️ Validation Rules

- A serial number **cannot exist twice** as `IN`
- A note must be `IN` before it can be `OUT`
- OCR confidence < 90% → force rescan
- Manual override requires admin login + reason

---

## 📊 Dashboard Metrics

- Live drawer balance
- Notes by denomination
- Today’s IN vs OUT
- Missing note detection
- Operator activity heatmap

---

## ⚠️ Known Challenges & Mitigations

### OCR Accuracy
**Mitigation**
- Fixed lighting
- Serial-region cropping
- Confidence threshold
- Forced rescans

### Speed of Operation
**Mitigation**
- Bundle scan mode (future)
- High-risk note focus (₹500 priority)

### Legal / Compliance
- System is **internal accounting**
- No bank CBS integration
- No RBI policy violation

---

## 🧠 Smart Deployment Strategy

### Phase 1 (MVP)
- ₹500 notes only
- Single operator
- Offline mode

### Phase 2
- Multi-denomination
- Operator login
- Advanced reports

### Phase 3
- Multi-branch support
- Central audit server
- AI anomaly detection

---

## 📌 Security Philosophy

> “Trust people less. Trust systems more.”

- Every note is accountable
- Every action is logged
- Every mismatch is explainable

---

## 🚀 Future Enhancements

- Bundle scanning (5 notes at once)
- Fingerprint / Face login
- CCTV snapshot per transaction
- SMS alert on mismatch
- Cloud sync (optional)

---

## 📜 Disclaimer

This software is intended for **internal cash management only**.  
It does not replace bank CBS systems and is not an RBI-regulated product.

---

## 👤 Author

**CNTS – Cash Note Tracking System**  
Designed for CSPs who want **control, clarity, and consequences**.

---
