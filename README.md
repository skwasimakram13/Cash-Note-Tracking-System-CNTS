# Cash Note Tracking System (CNTS)

> A computer vision–powered cash inflow and outflow control system for CSP and other cash-intensive businesses.

---

## 🧠 Problem Statement

Cash-based CSP operations commonly suffer from:

- Manual reconciliation errors  
- Employee-led note substitution or concealment  
- Zero traceability at the **individual banknote level**  
- End-of-day mismatches with no forensic evidence  

Traditional accounting systems track **amounts**.  
Fraud, however, happens at the **note level**.

**CNTS addresses this gap by digitizing every physical banknote.**

---

## 🎯 Objective

To build a desktop-based software system that:

- Detects Indian currency denominations (₹50 / ₹100 / ₹200 / ₹500)
- Reads and stores **unique banknote serial numbers** using a camera and OCR
- Tracks **IN / OUT** movement of each individual note
- Maintains a real-time cash drawer balance
- Prevents, detects, and audits internal cash theft

---

## 🏗️ System Architecture (High Level)

- USB Camera  
- Image Capture  
- Note Detection (Denomination)  
- Serial Number OCR  
- Validation Layer  
- Ledger Database  
- Dashboard & Reports  

This architecture creates a **Cash Digital Twin** of the physical drawer.

---

## 🖥️ Hardware Requirements

| Component      | Minimum Specification                     |
|---------------|--------------------------------------------|
| Desktop OS    | Windows 10 / Windows 11                    |
| Camera        | USB HD Camera (1080p, fixed focus)         |
| Mount         | Fixed overhead mount (non-movable)         |
| Lighting      | White LED lighting (diffused, shadow-free) |
| Desk Surface  | Matte black base                           |

⚠️ **Camera angle and lighting conditions must never change.**

---

## 🧰 Tech Stack

### Core
- **Python 3.10+**
- **OpenCV** – image preprocessing and enhancement
- **YOLOv8** – currency note denomination detection
- **Tesseract OCR** – serial number extraction

### Backend
- **SQLite** (local) or **PostgreSQL** (scalable)
- **SQLAlchemy ORM**

### Frontend (Desktop)
- **PyQt** or **Tkinter**
- Offline-first design (no internet dependency)

---

## 🧩 Key Features

### ✔ Denomination Detection
- Identifies ₹50 / ₹100 / ₹200 / ₹500 notes
- Confidence-score–based validation

### ✔ Serial Number OCR
- Serial-region cropping
- Image enhancement before OCR
- Regex-based serial validation
- OCR confidence threshold enforcement

### ✔ Cash In / Cash Out Workflow
- Mandatory scanning for every note
- No manual amount entry
- Automatic total calculation

### ✔ Anti-Theft Controls
- Duplicate serial number detection
- Withdraw-only-existing-notes rule
- Scan refusal on mismatches

### ✔ Audit & Reporting
- End-of-day reconciliation
- Operator-wise activity logs
- Missing note alerts

---

## 🔄 Operational Flow

### CASH IN (Deposit / Cash Received)

1. Operator selects **Cash In**
2. Notes are placed one by one under the camera
3. System detects:
   - Denomination  
   - Serial number  
4. Each note is stored with status `IN`
5. Drawer balance updates automatically

---

### CASH OUT (Withdrawal)

1. Operator selects **Cash Out**
2. Required withdrawal amount is displayed
3. Notes must be scanned individually
4. System verifies note availability
5. Notes are marked with status `OUT`

🚫 **No scan → No transaction**

---

## 🗃️ Database Schema

### `notes`

| Column         | Type        | Description              |
|---------------|-------------|--------------------------|
| serial_number | TEXT (PK)   | Unique banknote ID       |
| denomination  | INTEGER     | 50 / 100 / 200 / 500     |
| status        | TEXT        | IN / OUT                 |
| last_seen     | TIMESTAMP   | Last scan timestamp      |

---

### `transactions`

| Column        | Type        |
|--------------|-------------|
| id           | INTEGER (PK)|
| type         | TEXT (IN/OUT)|
| total_amount | INTEGER     |
| operator_id  | INTEGER     |
| timestamp    | TIMESTAMP   |

---

### `operators`

| Column    | Type    |
|----------|---------|
| id       | INTEGER |
| name     | TEXT    |
| login_id | TEXT    |

---

## 🛡️ Validation Rules

- A serial number **cannot exist twice** with status `IN`
- A note must be `IN` before it can be marked `OUT`
- OCR confidence below 90% triggers a forced rescan
- Manual overrides require admin login and justification

---

## 📊 Dashboard Metrics

- Live drawer balance
- Denomination-wise note count
- Today’s total IN vs OUT
- Missing note alerts
- Operator activity summary

---

## ⚠️ Known Challenges & Mitigations

### OCR Accuracy
**Mitigations**
- Fixed lighting and camera angle
- Precise serial-region cropping
- Confidence-based rescanning

### Operational Speed
**Mitigations**
- Planned bundle scan mode
- High-risk denomination prioritization (₹500 notes)

### Legal & Compliance
- System is for **internal accounting only**
- No integration with bank CBS systems
- No RBI regulatory dependency

---

## 🧠 Deployment Strategy

### Phase 1 – MVP
- ₹500 denomination only
- Single operator
- Fully offline mode

### Phase 2
- Multi-denomination support
- Operator authentication
- Advanced reporting

### Phase 3
- Multi-branch support
- Central audit server
- AI-based anomaly detection

---

## 📌 Security Philosophy

> “Trust people less. Trust systems more.”

- Every note is accountable  
- Every action is logged  
- Every discrepancy is explainable  

---

## 🚀 Future Enhancements

- Bundle scanning (multiple notes per scan)
- Fingerprint or face authentication
- CCTV snapshot capture per transaction
- SMS alerts for mismatches
- Optional cloud synchronization

---

## 📜 Disclaimer

This software is intended strictly for **internal cash management**.  
It does not replace bank CBS systems and is **not an RBI-regulated product**.

---

# Contribution Guide
- Fork repository
- Create branch: `feature/xxx` or `bugfix/yyy`
- Follow code style (Java: Android style guide)
- Create PR with description and linked issue
- CI must pass before merge


# License & Contact
- MIT License — you may use and modify the code for your organization. Include attribution if you redistribute.
- For commercial / closed-source product consider proprietary license.

**Contact**: Project owner / maintainer - wasim@demoody.com

---
## Author
**Develope By** - [Sk Wasim Akram](https://github.com/skwasimakram13)

- 👨‍💻 All of my projects are available at [https://skwasimakram.com](https://skwasimakram.com)

- 📝 I regularly write articles on [https://blog.skwasimakram.com](https://blog.skwasimakram.com)

- 📫 How to reach me **hello@skwasimakram.com**

- 🧑‍💻 Google Developer Profile [https://g.dev/skwasimakram](https://g.dev/skwasimakram)

- 📲 LinkedIn [https://www.linkedin.com/in/sk-wasim-akram](https://www.linkedin.com/in/sk-wasim-akram)

---

💡 *Built with ❤️ and creativity by Wassu.*

---

*This README is a product-level blueprint. It contains technical and legal notes and external policies evolve.*

