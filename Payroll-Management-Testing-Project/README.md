<div align="center">
  <img src="https://img.shields.io/badge/Payroll%20Management-Team%2011-1e3c72?style=for-the-badge&logo=appveyor" alt="Project Banner" />
  <h1 align="center">Payroll Management System 💻</h1>
  <p align="center">
    <b>An Advanced Academic Software Testing Showcase (A to Z)</b>
  </p>
  
  [![Python](https://img.shields.io/badge/Python-3.14-blue?style=flat-square&logo=python)](#)
  [![Flask](https://img.shields.io/badge/Flask-Framework-black?style=flat-square&logo=flask)](#)
  [![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=flat-square&logo=sqlite)](#)
  [![Testing](https://img.shields.io/badge/Coverage-99%25-success?style=flat-square)](#)
</div>

---

Welcome to the **Payroll Management System (System Under Test)** built specifically by **Team 11** for an advanced Software Testing academic exercise.

This repository is an exhaustive demonstration of the Software Testing Lifecycle (STLC). We built a functional web application, intentionally seeded it with defects, and systematically executed manual and automated tests against it using industry-standard techniques.

---

## 🏗️ 1. Dynamic Architecture Flow

The System Under Test (SUT) is built using a modern, lightweight web architecture. Below is the interactive flow of how our layers communicate:

```mermaid
graph TD
    %% Architecture Nodes
    subgraph Frontend ["🎨 View Layer: Glassmorphism UI"]
        UI("HTML5 / CSS3 / Jinja2")
    end
    
    subgraph Backend ["🧠 Controller & Service Layer: Flask"]
        API("Web Routes")
        SVC("Payroll Logic Services")
    end
    
    subgraph Database ["💾 Data Layer: SQLite"]
        DB[("Relational DB")]
    end

    %% Flow connections
    UI -->|"HTTP GET/POST"| API
    API -->|"Orchestrates"| SVC
    SVC -->|"SQLAlchemy ORM Queries"| DB
    DB -->|"Returns Result Set"| SVC
    SVC -->|"Processes Logic & Tax"| API
    API -->|"Renders State"| UI
```

---

## 🧪 2. Testing Techniques & Evidence Mapping

We separated our testing artifacts into highly organized directories. Below is the interactive map showing which folders correspond to which testing techniques:

```mermaid
graph LR
    Root(("🚀 Software Testing")) --> BB{"⬛ Black Box"}
    Root --> WB{"🩻 White Box"}
    Root --> IT{"🔗 Integration"}

    %% Black Box Branch
    BB --> BB1["BVA & ECP"]
    BB --> BB2["Cause-Effect & Decision Table"]
    BB1 -.-> |"Screenshots"| F1("📂 evidence/black_box")
    BB2 -.-> |"Defect Captures"| F2("📂 evidence/initial_failures")

    %% White Box Branch
    WB --> WB1["Statement Coverage"]
    WB --> WB2["Branch Coverage"]
    WB1 -.-> |"Pytest HTML"| F3("📂 evidence/white_box")
    WB2 -.-> F3

    %% Integration Branch
    IT --> IT1["End-to-End Flow"]
    IT --> IT2["DB Cascades"]
    IT1 -.-> |"Pytest-HTML Reports"| F4("📂 evidence/integration")
    IT2 -.-> F4

    %% Styles for attractiveness
    style Root fill:#ff9a9e,stroke:#fff,stroke-width:2px,color:#fff
    style BB fill:#2c3e50,stroke:#fff,stroke-width:2px,color:#fff
    style WB fill:#bdc3c7,stroke:#fff,stroke-width:2px,color:#2c3e50
    style IT fill:#16a085,stroke:#fff,stroke-width:2px,color:#fff
    
    style F1 fill:#f39c12,stroke:#fff,stroke-width:1px,color:#fff
    style F2 fill:#e74c3c,stroke:#fff,stroke-width:1px,color:#fff
    style F3 fill:#2980b9,stroke:#fff,stroke-width:1px,color:#fff
    style F4 fill:#27ae60,stroke:#fff,stroke-width:1px,color:#fff
```

---

## 📖 3. Detailed Explanation of Techniques

### ⬛ A. Black-Box Testing
*Testing functionality without peering into internal code structures. Driven by Playwright UI automation.*
- **Equivalence Class Partitioning (ECP)**: Dividing data into valid/invalid partitions. We used this on Employee form fields (e.g., Names only accept alphabets).
- **Boundary Value Analysis (BVA)**: Testing the extreme edges of ranges to catch off-by-one errors. We used this for Basic Salary bounds (`10,000` to `500,000`).
- **Cause-Effect Graphing**: Mapping specific inputs to specific outcomes. Used for Attendance logic (e.g., rejecting submissions where `Present Days > Working Days`).
- **Decision Table Testing**: Used for complex multi-condition rules, specifically our Income Tax brackets (10% vs 20%) and Professional Tax evaluations.

### 🩻 B. White-Box Testing
*Testing the internal code structures and logic paths. Driven by Pytest and Pytest-Cov.*
- **Statement & Branch Coverage**: We wrote automated unit tests targeting `app/services/payroll_service.py` to ensure every mathematical operation, IF statement, and edge case is executed by a test. **(Achieved 99% Code Coverage)**.

### 🔗 C. Integration Testing
*Testing communication between components. Driven by Pytest end-to-end endpoints.*
- Verified that submitting an employee via the UI Route successfully inserts data into the SQLite Database, and successfully triggers the automated Salary configuration Service in cascade.

---

## 📋 4. Test Cases & Defect Summary (The "A to Z")

We executed **73 total Test Cases** during our cycle. We intentionally seeded the app with defects, captured them in `evidence/initial_failures`, fixed them, and re-tested them.

<div align="center">

| Test ID | Module | Technique | Test Scenario | Status | Defect Found |
|:-------:|:-------|:----------|:--------------|:------:|:-------------|
| **TC-001** | Authentication | Positive | Login with valid credentials | ✅ Pass | - |
| **TC-012** | Employee | BVA | Basic Salary = ₹500,000 | ❌ Fail | **BUG-001** (Accepted invalid boundary) |
| **TC-021** | Attendance | Cause-Effect | Present Days > Working Days | ❌ Fail | **BUG-002** (Bypassed logic) |
| **TC-030** | Payroll | Decision Table | Calculate Gross Salary | ❌ Fail | **BUG-003** (Conveyance omitted) |
| **TC-031** | Payroll | Decision Table | Tax Calc for Salary > 30k | ❌ Fail | **BUG-005** (Calculated at 10% not 20%) |
| **TC-034** | Payroll | State Transition | Generate Payroll same month, diff year | ❌ Fail | **BUG-004** (Falsely flagged duplicate) |
| **TC-040** | Dashboard | UI/UX | Verify Analytics Panel Title | ❌ Fail | **BUG-010** (Typo injected) |

</div>

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

**3. View the Interactive Presentation Materials**
Open **`presentation_test_sheet.html`** in your browser for a stunning, interactive DataTables matrix of our test cases! Alternatively, open the generated assets inside the `report/` (DOCX) and `presentation/` (PPTX) folders.

---
<div align="center">
  <i>Developed & Tested by Team 11</i>
</div>
