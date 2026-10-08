# Defect Report
**Project:** Payroll Management System
**Team:** Team 11

## Defect Summary
During the manual execution phase, 5 defects were identified in the business logic of the application. These defects impact salary calculations, attendance validations, boundary rules, and application state.

---

### Defect 1: BUG-001
- **Module:** Employee Management (Add Employee)
- **Description:** The system allows an employee to be added with a basic salary of exactly ₹500,000, despite the business rule stating the maximum limit is *strictly less than* 500,000.
- **Steps to Reproduce:**
  1. Navigate to Add Employee form.
  2. Fill in all required fields.
  3. Enter `500000` in the Basic Salary field.
  4. Submit the form.
- **Expected Result:** Validation error indicating salary must be less than 500,000.
- **Actual Result:** Employee is successfully added (Boundary Value Analysis failure).
- **Severity:** Medium
- **Status:** Open

### Defect 2: BUG-002
- **Module:** Attendance Management
- **Description:** The system fails to validate that present days cannot exceed working days if the leave days are exactly zero. The validation logic is incorrectly bypassed.
- **Steps to Reproduce:**
  1. Navigate to Add Attendance.
  2. Enter Working Days = 30.
  3. Enter Present Days = 35.
  4. Enter Leave Days = 0.
  5. Submit the form.
- **Expected Result:** Validation error stating present days cannot exceed working days.
- **Actual Result:** The record is saved successfully.
- **Severity:** High
- **Status:** Open

### Defect 3: BUG-003
- **Module:** Salary Processing
- **Description:** Conveyance allowance is completely omitted when calculating the Gross Salary, resulting in underpayment.
- **Steps to Reproduce:**
  1. Navigate to Salary Components for EMP001.
  2. Observe the Earnings breakdown.
  3. Manually sum Basic + HRA + DA + Conveyance + Other Allowance.
- **Expected Result:** The displayed Gross Salary should equal the sum of all earnings components.
- **Actual Result:** The Gross Salary is short by the exact amount of the Conveyance allowance.
- **Severity:** Critical
- **Status:** Open

### Defect 4: BUG-004
- **Module:** Payroll Generation
- **Description:** The system prevents generating payroll for a different year if a payroll for that month already exists. The duplicate check ignores the year field entirely.
- **Steps to Reproduce:**
  1. Generate payroll for EMP001 for September 2026.
  2. Attempt to generate payroll for EMP001 for September 2027.
- **Expected Result:** Payroll for September 2027 should be generated successfully.
- **Actual Result:** System returns an error: "Payroll for this month already exists".
- **Severity:** High
- **Status:** Open

### Defect 5: BUG-005
- **Module:** Payroll Generation (Tax Calculation)
- **Description:** For gross salaries over ₹100,000, the income tax is incorrectly calculated at 10% instead of the mandated 20%.
- **Steps to Reproduce:**
  1. Create an employee with a high basic salary such that Gross Salary > 100,000.
  2. Generate their payroll.
  3. Check the calculated Income Tax deduction.
- **Expected Result:** Income tax should be calculated as 20% of Gross Salary.
- **Actual Result:** Income tax is calculated as 10% of Gross Salary.
- **Severity:** Critical
- **Status:** Open

---
*End of Report*
