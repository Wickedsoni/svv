# 🏢 Payroll Management System - Academic Software Testing Project

![Python](https://img.shields.io/badge/Python-3.14-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-Framework-black?style=for-the-badge&logo=flask)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite)
![Testing](https://img.shields.io/badge/Software_Testing-Academic-success?style=for-the-badge)

Welcome to the **Payroll Management System (System Under Test)** built specifically by **Team 11** for an advanced Software Testing academic exercise.

This repository is an exhaustive A-to-Z demonstration of the Software Testing Lifecycle (STLC). We built a functional, modern web application, intentionally seeded it with defects, and systematically executed manual and automated tests against it using industry-standard techniques.

---

## 🏗️ 1. Project Architecture

The System Under Test (SUT) is built using a modern, lightweight web architecture:

- **Backend Logic (Controller/Service)**: Written in **Python** using the **Flask** microframework. 
- **Database (Model)**: **SQLite** with **SQLAlchemy** ORM for relational data mapping (Employees, Attendance, Payroll, Salary Components).
- **Frontend (View)**: **HTML5**, **Vanilla CSS**, and **Jinja2** templates. The UI is designed using premium **Glassmorphism**, vibrant gradients, and dynamic micro-animations to simulate a modern enterprise application.
- **Automation & Testing Engines**: **PyTest**, **PyTest-Cov**, **PyTest-HTML**, and **Playwright** (for headless browser automation).

---

## 🧪 2. Software Testing Techniques Applied

We applied rigorous academic testing techniques to discover defects, validate business logic, and ensure system reliability. 

### ⬛ A. Black-Box Testing
*Testing the software's functionality without peering into its internal code structures.*
- **Equivalence Class Partitioning (ECP)**: We divided input data into valid and invalid partitions. 
  - *Where we used it*: Employee Creation fields (validating Name accepts alphabetical characters, preventing numeric/special characters).
- **Boundary Value Analysis (BVA)**: We tested the extreme boundaries of input ranges to catch off-by-one errors.
  - *Where we used it*: Basic Salary limits. The rule states salary must be `≥ ₹10,000` and `< ₹500,000`. We tested exactly `9,999`, `10,000`, `499,999`, and `500,000`.
- **Cause-Effect Graphing**: Mapping specific combinations of inputs (causes) to specific outputs (effects).
  - *Where we used it*: Attendance Management. (e.g., *If Leave Days = 0 AND Present Days > Working Days, then Reject*).
- **Decision Table Testing**: Used for complex business rules that depend on multiple logical conditions.
  - *Where we used it*: Tax and Payroll calculations. (e.g., *If Gross > 30k -> Tax = 20%. If Gross <= 30k -> Tax = 10%*).

### 🩻 B. White-Box Testing
*Testing the internal code structures, logic, and paths.*
- **Statement & Branch Coverage**: We wrote automated unit tests that execute specific functions in the backend to ensure every line of code is hit.
- *Where we used it*: The core `app/services/payroll_service.py` which handles the complex math. We achieved a **99% Statement Coverage**.

### 🔗 C. Integration Testing
*Testing the communication and data flow between integrated components.*
- *Where we used it*: End-to-end integration flows. We verified that submitting an employee via the Route successfully inserted data into the Database, which successfully triggered the Salary configuration Service.

---

## 📁 3. Repository Directory Structure

Every testing artifact and codebase module is organized meticulously:

```text
├── app/                            # System Under Test (SUT) Source Code
│   ├── database/                   # SQLite initialization and bug-seeding
│   ├── routes/                     # Flask web controllers
│   ├── services/                   # Business logic (Target of White-Box testing)
│   └── templates/                  # Glassmorphism UI (Target of Black-Box UI testing)
├── evidence/                       # 📸 The Core Evidence Directory (40+ Screenshots)
│   ├── black_box/                  # Screenshots of Boundary/ECP testing in the UI
│   ├── initial_failures/           # Screenshots of intentional UI/Logic bugs captured before fixing
│   ├── integration/                # Screenshots of the automated Integration Test HTML reports
│   └── white_box/                  # Screenshots of Pytest-Cov Line-by-Line Code Coverage
├── presentation/                   # Academic Presentation Assets
│   └── Testing_Presentation.pptx   # 16-slide PowerPoint summarizing the project
├── report/                         # Academic Document Assets
│   └── Final_Testing_Document.docx # 28+ Page formal document written in ASD-STE100
├── test-cases/                     # Manual Testing Documentation
│   ├── defects_report.md           # Deep dive into the 5 injected defects
│   └── manual_test_cases.xlsx      # Master spreadsheet of all 73 test cases
├── tests/                          # Automated Testing Scripts
│   └── test_integration.py         # Pytest integration suite
├── capture_testing_evidence.py     # Playwright automation script to generate evidence
├── presentation_test_sheet.html    # Interactive Web-based Test Execution Matrix
└── run.py                          # Entry point to start the application
```

---

## 📋 4. Test Cases & Execution Summary

We designed and executed a total of **73 Test Cases**. Below is a summary of the critical cases that highlight our techniques:

| Test ID | Module | Technique | Test Scenario | Status | Defect Found |
|---------|--------|-----------|---------------|--------|--------------|
| **TC-001** | Authentication | Positive | Login with valid credentials | Pass | - |
| **TC-012** | Employee | BVA | Basic Salary = ₹500,000 | Fail | BUG-001 (Accepted invalid boundary) |
| **TC-021** | Attendance | Cause-Effect | Present Days > Working Days | Fail | BUG-002 (Bypassed logic) |
| **TC-030** | Payroll | Decision Table | Calculate Gross Salary | Fail | BUG-003 (Conveyance omitted) |
| **TC-031** | Payroll | Decision Table | Tax Calc for Salary > 30k | Fail | BUG-005 (Calculated at 10% instead of 20%) |
| **TC-034** | Payroll | State Transition | Generate Payroll for same month, diff year | Fail | BUG-004 (Falsely flagged as duplicate) |
| **TC-040** | Dashboard | UI/UX | Verify Analytics Panel Title | Fail | BUG-010 (Typo injected) |

### 🐛 The Defect Lifecycle
We intentionally seeded the application with defects. We documented them, captured visual evidence of their failure in the UI (stored in `evidence/initial_failures`), fixed the underlying code in `app/services/payroll_service.py` and `app/templates/`, and re-tested the system to ensure passing status.

---

## 🚀 5. How to Run the Project

**1. Install Dependencies**
```bash
pip install flask flask-sqlalchemy pytest pytest-cov pytest-html playwright python-docx python-pptx
playwright install chromium
```

**2. Start the Application**
```bash
python run.py
```
*Access the beautiful Glassmorphism UI at `http://127.0.0.1:5000` (Creds: admin / admin123)*

**3. Run the Automated Test Suite**
```bash
pytest tests/test_integration.py --cov=app --html=report_integration.html
```

**4. View the Presentation Materials**
Open `presentation_test_sheet.html` in your browser for a stunning, interactive DataTables matrix of our test cases, or open the generated assets inside the `report/` and `presentation/` folders!

---
*Developed & Tested by Team 11*
