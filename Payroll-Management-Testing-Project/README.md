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
        UI("HTML5 / CSS3 / Bootstrap 5 / Jinja2")
    end
    
    subgraph Backend ["🧠 Controller & Service Layer: Flask"]
        API("Web Routes (auth, dashboard, employees)")
        SVC("Payroll Logic Services (Tax, Salary, DB)")
    end
    
    subgraph Database ["💾 Data Layer: SQLite"]
        DB[("Relational DB (SQLAlchemy ORM)")]
    end

    %% Flow connections
    UI -->|"HTTP GET/POST (User Action)"| API
    API -->|"Orchestrates Business Logic"| SVC
    SVC -->|"SQLAlchemy ORM Queries (CRUD)"| DB
    DB -->|"Returns Result Set / Confirms Write"| SVC
    SVC -->|"Processes Logic & Tax Math"| API
    API -->|"Renders State to Template"| UI
```

---

## 🧪 2. Testing Techniques & Evidence Mapping

We separated our testing artifacts into highly organized directories. Below is the detailed interactive map showing which folders correspond to which testing techniques:

```mermaid
graph LR
    Root(("🚀 Software Testing Lifecycle")) --> BB{"⬛ Black Box"}
    Root --> WB{"🩻 White Box"}
    Root --> IT{"🔗 Integration"}

    %% Black Box Branch
    BB --> BB1["BVA (Boundaries)"]
    BB --> BB2["ECP (Partitions)"]
    BB --> BB3["Cause-Effect & Decision Table"]
    BB1 -.-> |"Playwright Screenshots"| F1("📂 evidence/black_box")
    BB2 -.-> F1
    BB3 -.-> |"Captured Intentional UI Bugs"| F2("📂 evidence/initial_failures")

    %% White Box Branch
    WB --> WB1["Statement Coverage (99%)"]
    WB --> WB2["Branch Coverage"]
    WB1 -.-> |"Pytest-Cov HTML Reports"| F3("📂 evidence/white_box")
    WB2 -.-> F3

    %% Integration Branch
    IT --> IT1["End-to-End API Flow"]
    IT --> IT2["DB Cascade Integrity"]
    IT1 -.-> |"Pytest-HTML Visual Reports"| F4("📂 evidence/integration")
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
*Testing functionality and UI behavior without peering into internal code structures. Driven by Playwright UI automation and manual execution.*

<div align="center">
  <img src="assets/bb_folder.svg" alt="Black Box Folder Mapping" width="600">
</div>

- **Equivalence Class Partitioning (ECP)**: Dividing data into valid/invalid partitions to ensure our forms reject malicious or incorrectly typed data. We used this on Employee form fields (e.g., verifying Names only accept alphabets, and Emails require the `@` symbol).
- **Boundary Value Analysis (BVA)**: Testing the extreme edges of ranges to catch off-by-one errors. We heavily utilized this for Basic Salary bounds (mandated to be strictly between `10,000` and `500,000`). We caught a critical defect by testing exactly `500,000`.
- **Cause-Effect Graphing**: Mapping specific inputs to specific conditional outcomes. Used for our Attendance logic (e.g., automatically rejecting submissions where `Present Days > Working Days`).
- **Decision Table Testing**: Used for complex multi-condition business rules, specifically our Income Tax brackets (10% vs 20% calculations) and Professional Tax evaluations across different salary bands.

### 🩻 B. White-Box Testing
*Testing the internal code structures, logic paths, and mathematical algorithms. Driven by Pytest and Pytest-Cov.*

<div align="center">
  <img src="assets/wb_folder.svg" alt="White Box Folder Mapping" width="600">
</div>

- **Statement Coverage**: We wrote automated unit tests targeting the `app/services/payroll_service.py` to ensure every single mathematical operation, tax bracket evaluation, and variable assignment is executed by a test at least once. **(Achieved 99% Code Coverage)**.
- **Branch Coverage**: We validated every `if/else` condition in the backend controllers to ensure that both the True and False evaluation paths of our business rules were actively verified.

### 🔗 C. Integration Testing
*Testing communication between connected systems and modules. Driven by Pytest end-to-end endpoints.*

<div align="center">
  <img src="assets/it_folder.svg" alt="Integration Folder Mapping" width="600">
</div>

- **End-to-End API Flow**: Verified that submitting a form on the UI Route successfully triggers the correct Flask controller, which in turn orchestrates the Salary Service.
- **Database Cascades (DB Integrity)**: Ensured that when data is inserted via the application layer, it accurately reflects in the SQLite Database, and that related foreign-key fields (like linking Attendance to the correct Employee ID) maintain perfect referential integrity.

---

## 📋 4. Test Cases & Defect Resolution (The "A to Z")

We executed **73 total Test Cases** during our cycle. We intentionally seeded the app with defects, captured them in `evidence/initial_failures`, fixed them, and re-tested them.

### Comprehensive Test Case Matrix (Top 11 Defects)

<div align="center">

| Test ID | Module | Technique | Test Scenario | Status | Defect Found |
|:-------:|:-------|:----------|:--------------|:------:|:-------------|
| **TC-010** | Employee | ECP | Add employee with numeric name | ❌ Fail | **BUG-006** (Accepted numeric characters) |
| **TC-011** | Employee | ECP | Submit form with valid data | ❌ Fail | **BUG-011** (Flash Message Color) |
| **TC-012** | Employee | BVA (Max) | Basic Salary = ₹500,000 | ❌ Fail | **BUG-001** (Accepted invalid boundary) |
| **TC-020** | Attendance | BVA (Zero)| Working Days = 0 | ❌ Fail | **BUG-007** (Caused ZeroDivisionError) |
| **TC-021** | Attendance | Cause-Effect | Present Days > Working Days | ❌ Fail | **BUG-002** (Bypassed logic via 0 leave) |
| **TC-030** | Payroll | Decision Table | Calculate Gross Salary | ❌ Fail | **BUG-003** (Conveyance omitted from gross) |
| **TC-031** | Payroll | Decision Table | Tax Calc for Salary > 30k | ❌ Fail | **BUG-005** (Calculated at 10% not 20%) |
| **TC-032** | Payroll | Decision Table | Calculate Professional Tax | ❌ Fail | **BUG-008** (Hardcoded to return 0) |
| **TC-034** | Payroll | State Transition | Payroll same month, diff year | ❌ Fail | **BUG-004** (Falsely flagged as duplicate) |
| **TC-040** | Dashboard | UI/UX | Verify Analytics Panel Title | ❌ Fail | **BUG-010** (Typo injected in UI HTML) |
| **TC-050** | Auth | State Transition | Access /payroll without login | ❌ Fail | **BUG-009** (Unauthorized Access bypass) |

</div>

### 🛠️ How We Resolved The Defects

During our defect lifecycle, we meticulously fixed all identified bugs. Here is exactly how we resolved our top 10 major logical failures:

#### 1. BUG-001: Boundary Value Analysis Failure
- **The Bug**: The system incorrectly allowed a Basic Salary of exactly ₹500,000, violating the strictly less than rule.
- **The Fix**: We updated the comparison operator in the validation route from `>=` to `>`.
  ```python
  # Before
  if basic_salary >= 500000:
  
  # After
  if basic_salary > 500000:
  ```

#### 2. BUG-002: Cause-Effect Validation Bypass
- **The Bug**: The system bypassed the critical validation check (`Present Days > Working Days`) if the user inputted `0` for Leave Days.
- **The Fix**: We decoupled the validation so it runs regardless of the leave days input.
  ```python
  # Before
  if leave_days == 0 and present_days > working_days:
      pass # Intentionally flawed bypass
  
  # After
  if present_days > working_days:
      raise ValueError("Present days cannot exceed working days.")
  ```

#### 3. BUG-003: Decision Table Gross Salary Miscalculation
- **The Bug**: The system was omitting the employee's conveyance allowance from the Gross Salary total.
- **The Fix**: We added `conveyance` to the `sum()` formula in `payroll_service.py`.
  ```python
  # Before
  gross = basic + hra + special_allowance
  
  # After
  gross = basic + hra + conveyance + special_allowance
  ```

#### 4. BUG-004: State Transition Date Checking Error
- **The Bug**: The application blocked generating payrolls for the same month across different years (e.g., Nov 2025 collided with Nov 2026).
- **The Fix**: We added year validation into the duplicate check query.
  ```python
  # Before
  duplicate = Payroll.query.filter_by(month=current_month).first()
  
  # After
  duplicate = Payroll.query.filter_by(month=current_month, year=current_year).first()
  ```

#### 5. BUG-005: Decision Table Tax Rule Violation
- **The Bug**: For employees with a gross salary over ₹30,000, income tax was calculated at a flat 10% instead of the mandated 20% bracket.
- **The Fix**: We updated the constant multiplier in the calculation engine.
  ```python
  # Before
  if gross_salary > 30000:
      income_tax = gross_salary * 0.10
      
  # After
  if gross_salary > 30000:
      income_tax = gross_salary * 0.20
  ```

#### 6. BUG-006: ECP Numeric Type Leak
- **The Bug**: The Employee form accepted numeric characters in the first and last name fields, breaking database hygiene.
- **The Fix**: We added a Regex match in the route controller.
  ```python
  # Before
  if not first_name:
      flash("Name is required")
      
  # After
  if not first_name.isalpha():
      flash("Name must contain only alphabets")
  ```

#### 7. BUG-007: ZeroDivisionError Crash
- **The Bug**: If Working Days were submitted as `0`, the attendance calculation raised an unhandled `ZeroDivisionError`.
- **The Fix**: We enforced a minimum of 1 working day in the form payload check.
  ```python
  # Before
  attendance_percentage = (present / working_days) * 100
  
  # After
  if working_days <= 0:
      raise ValueError("Working days must be greater than zero.")
  attendance_percentage = (present / working_days) * 100
  ```

#### 8. BUG-008: Hardcoded Professional Tax
- **The Bug**: Professional tax calculation always returned 0 regardless of salary bracket.
- **The Fix**: We replaced the hardcoded `0` with the actual bracket calculation dictionary.
  ```python
  # Before
  def calculate_prof_tax(salary):
      return 0
      
  # After
  def calculate_prof_tax(salary):
      if salary > 20000: return 200
      return 150
  ```

#### 9. BUG-009: Unauthorized Access Bypass
- **The Bug**: Users could bypass the login screen and directly access `http://127.0.0.1:5000/payroll` by typing the URL.
- **The Fix**: We added the Flask `@login_required` decorator to the Payroll controller routes.
  ```python
  # Before
  @bp.route('/payroll')
  def view_payroll():
      return render_template('payroll/index.html')
      
  # After
  @bp.route('/payroll')
  @login_required
  def view_payroll():
      return render_template('payroll/index.html')
  ```

#### 10. BUG-010: UI Typo in Analytics Panel
- **The Bug**: The main dashboard header incorrectly displayed "Analitics Overview".
- **The Fix**: We corrected the typo in the Jinja2 template (`dashboard.html`).
  ```html
  <!-- Before -->
  <h2 class="panel-title">Analitics Overview</h2>
  
  <!-- After -->
  <h2 class="panel-title">Analytics Overview</h2>
  ```

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
