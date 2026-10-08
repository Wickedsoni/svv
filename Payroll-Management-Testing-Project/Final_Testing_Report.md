# Final Software Testing Report
**Project Name:** Payroll Management System
**Team:** 11
**Date:** October 8, 2026

## 1. Executive Summary
This report documents the academic software testing exercise performed on the Payroll Management System (System Under Test - SUT). The primary objective was to demonstrate practical software testing techniques, including test scenario design, manual test execution using Boundary Value Analysis (BVA) and Equivalence Class Partitioning (ECP), defect identification, and white-box coverage analysis.

Overall, the system was thoroughly tested. **73 manual test cases** were designed and executed. During execution, **5 intentional defects** were identified, logged, and subsequently fixed. Post-fix validation confirms that the business logic now operates correctly with **99% automated code coverage**.

---

## 2. Test Scope & Methodology
### 2.1 Scope
The testing scope encompassed the core modules of the Payroll Management System:
- Employee Management (CRUD operations, validation rules)
- Attendance Management (Validation of working days, present days, leaves)
- Salary Component Configuration
- Payroll Generation (Calculations for Gross Salary, Net Salary, Deductions, and Taxes)

### 2.2 Methodology
- **Black-Box Testing:** Utilized BVA and ECP to generate test cases for input fields (e.g., basic salary boundaries, attendance day boundaries). Cause-Effect graphing and Decision Table logic were applied to state-based rules like duplicate payroll generation.
- **White-Box Testing:** Implemented automated unit tests using `pytest` to achieve Statement and Branch coverage of the core backend service (`payroll_service.py`).
- **Defect Lifecycle:** Bugs were identified, documented, fixed, and retested.

---

## 3. Test Execution Summary
- **Total Test Cases Designed:** 73
- **Test Cases Passed (Initial Run):** 68
- **Test Cases Failed (Initial Run):** 5
- **Automated Tests:** 9 unit tests generated.
- **Code Coverage (Backend Services):** 99%

*Note: The comprehensive test cases are available in the accompanying `test-cases/manual_test_cases.xlsx` file.*

---

## 4. Defect Report & Resolution
During the manual execution phase, 5 critical defects were discovered in the application's business logic.

### BUG-001: Salary Boundary Validation Failure
- **Description:** The system allowed a Basic Salary of exactly ₹500,000, violating the strictly-less-than (< 500,000) business rule.
- **Root Cause:** Defective logic using `>=` instead of `>`.
- **Resolution:** Fixed the logic operator. Re-tested successfully.

### BUG-002: Attendance Validation Bypass
- **Description:** When `leave_days` was exactly 0, the system bypassed the check ensuring `present_days` could not exceed `working_days`.
- **Root Cause:** Flawed conditional logic (`if leave_days == 0 and present_days > working_days` instead of isolated checks).
- **Resolution:** Removed the flawed `leave_days == 0` bypass. Re-tested successfully.

### BUG-003: Incorrect Gross Salary Calculation
- **Description:** The Conveyance Allowance was systematically omitted from the Gross Salary calculation.
- **Root Cause:** The `conveyance` variable was missing from the sum in `calculate_gross_salary`.
- **Resolution:** Added `conveyance` to the calculation logic. Re-tested successfully.

### BUG-004: Duplicate Payroll Detection Flaw
- **Description:** The system falsely blocked payroll generation for the same month in different years (e.g., Sep 2026 vs Sep 2027) because the year was ignored.
- **Root Cause:** The database query lacked a filter for the `year` field.
- **Resolution:** Included `year=year` in the duplicate query filter. Re-tested successfully.

### BUG-005: Income Tax Rate Error
- **Description:** For salaries > ₹30,000, the income tax was calculated at 10% instead of the specified 20%.
- **Root Cause:** Hardcoded constant `0.10` instead of `0.20`.
- **Resolution:** Updated the multiplier to `0.20`. Re-tested successfully.

---

## 5. Automated White-Box Testing (Code Coverage)
Using `pytest` and `pytest-cov`, a suite of automated unit tests was created against `app/services/payroll_service.py`.

**Coverage Results:**
- **Module:** `app.services.payroll_service`
- **Total Statements:** 177
- **Missed Statements:** 2
- **Coverage Percentage:** 99%

This exceeds the academic project requirement of 90%+ code coverage. The tests successfully validate boundary limits, input sanitization, complex calculations, and state rules (like active employee checks).

---

## 6. Conclusion and Sign-off
The Payroll Management System has been fully verified according to academic software testing principles. All test scenarios have been documented, intentional bugs have been identified and resolved, and the codebase demonstrates exceptional automated test coverage. 

**Status:** Project complete and ready for academic submission.

*Signed, Team 11*
