"""
Payroll Business Logic Services
Team 11 — Manual Testing Demo Application

IMPORTANT: Simplified payroll calculation rules for academic demonstration only.
These do not represent statutory payroll compliance.

NOTE: This file contains 5 intentionally seeded academic defects for testing demonstration.
See internal/seeded_defects.md for details.
"""
import re
from datetime import datetime


# ─────────────────────────────────────────────
# VALIDATION FUNCTIONS
# ─────────────────────────────────────────────

def validate_employee_id(employee_id: str) -> dict:
    """
    Validate employee ID.
    Pattern: EMP followed by exactly 3 digits (EMP001 to EMP999).
    """
    if not employee_id:
        return {'valid': False, 'message': 'Employee ID is required.'}
    
    pattern = r'^EMP\d{3}$'
    if not re.match(pattern, employee_id):
        return {'valid': False, 'message': 'Employee ID must be in format EMP001 to EMP999 (EMP + exactly 3 digits).'}
    
    return {'valid': True, 'message': 'Valid Employee ID.'}


def validate_employee_name(name: str) -> dict:
    """
    Validate employee name.
    Must be 2–50 characters. Must not be numeric-only.
    """
    if not name or not name.strip():
        return {'valid': False, 'message': 'Employee Name is required.'}
    
    name = name.strip()
    
    if len(name) < 2:
        return {'valid': False, 'message': 'Employee Name must be at least 2 characters.'}
    
    if len(name) > 50:
        return {'valid': False, 'message': 'Employee Name must not exceed 50 characters.'}
    
    # DEFECT 6 (BUG-006): Intentionally bypassed numeric name check
    # if name.isdigit():
    #     return {'valid': False, 'message': 'Employee Name cannot be numeric only.'}
    
    return {'valid': True, 'message': 'Valid name.'}


def validate_email(email: str) -> dict:
    """
    Validate email address format.
    """
    if not email or not email.strip():
        return {'valid': False, 'message': 'Email is required.'}
    
    pattern = r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email.strip()):
        return {'valid': False, 'message': 'Invalid email format.'}
    
    return {'valid': True, 'message': 'Valid email.'}


def validate_phone(phone: str) -> dict:
    """
    Validate Indian mobile number.
    Must be 10 digits, starting with 6, 7, 8, or 9.
    """
    if not phone or not phone.strip():
        return {'valid': False, 'message': 'Phone number is required.'}
    
    phone = phone.strip()
    pattern = r'^[6789]\d{9}$'
    if not re.match(pattern, phone):
        return {'valid': False, 'message': 'Phone must be 10 digits starting with 6, 7, 8, or 9.'}
    
    return {'valid': True, 'message': 'Valid phone number.'}


def validate_basic_salary(salary) -> dict:
    """
    Validate basic salary.
    Valid range: 10000 to 500000 (inclusive).

    SEEDED DEFECT 1 (BUG-001):
    The upper boundary check uses strict less-than (<) instead of
    less-than-or-equal (<=), causing 500000 to be incorrectly rejected.
    Original correct code:  salary > 500000
    Defective code:         salary >= 500000
    """
    try:
        salary = float(salary)
    except (TypeError, ValueError):
        return {'valid': False, 'message': 'Basic Salary must be a numeric value.'}
    
    if salary < 10000:
        return {'valid': False, 'message': 'Basic Salary must be at least ₹10,000.'}
    
    # DEFECT 1 FIXED: Use strict greater-than (>) instead of >=
    if salary > 500000:
        return {'valid': False, 'message': 'Basic Salary must not exceed ₹500,000.'}
    
    return {'valid': True, 'message': 'Valid salary.'}


def validate_attendance(working_days, present_days, leave_days, overtime_hours) -> dict:
    """
    Validate attendance data.
    Working Days: 1–31
    Present Days: 0–working_days
    Leave Days: 0–working_days
    Present + Leave <= Working Days
    Overtime: 0–100

    SEEDED DEFECT 2 (BUG-002):
    The check for present_days > working_days is missing when leave_days > 0,
    so the combined sum validation fires but individual present_days cap is
    only checked when leave_days == 0.
    This allows present_days = working_days + 1 to pass if leave_days = 0.
    Actually implemented as: present_days check is using > instead of >=
    allowing present_days == working_days + 1 through a specific path.
    """
    try:
        working_days = int(working_days)
        present_days = int(present_days)
        leave_days = int(leave_days)
        overtime_hours = float(overtime_hours)
    except (TypeError, ValueError):
        return {'valid': False, 'message': 'All attendance fields must be numeric.'}
    
    if working_days < 1 or working_days > 31:
        return {'valid': False, 'message': 'Working Days must be between 1 and 31.'}
    
    if present_days < 0:
        return {'valid': False, 'message': 'Present Days cannot be negative.'}
    
    # DEFECT 2 FIXED: Removed the leave_days == 0 bypass
    if present_days > working_days:
        return {'valid': False, 'message': 'Present Days cannot exceed Working Days.'}
    
    if leave_days < 0:
        return {'valid': False, 'message': 'Leave Days cannot be negative.'}
    
    if present_days + leave_days > working_days:
        return {'valid': False, 'message': 'Present Days + Leave Days cannot exceed Working Days.'}
    
    # DEFECT 7 (BUG-007): Bypassed negative overtime hours check
    # if overtime_hours < 0:
    #     return {'valid': False, 'message': 'Overtime Hours cannot be negative.'}
    
    if overtime_hours > 100:
        return {'valid': False, 'message': 'Overtime Hours cannot exceed 100 per month.'}
    
    return {'valid': True, 'message': 'Valid attendance.'}


def validate_other_allowance(amount) -> dict:
    """Validate other allowance — must be non-negative."""
    try:
        amount = float(amount)
    except (TypeError, ValueError):
        return {'valid': False, 'message': 'Other Allowance must be numeric.'}
    
    if amount < 0:
        return {'valid': False, 'message': 'Other Allowance cannot be negative.'}
    
    return {'valid': True, 'message': 'Valid.'}


def validate_other_deductions(amount) -> dict:
    """Validate other deductions — must be non-negative."""
    try:
        amount = float(amount)
    except (TypeError, ValueError):
        return {'valid': False, 'message': 'Other Deductions must be numeric.'}
    
    if amount < 0:
        return {'valid': False, 'message': 'Other Deductions cannot be negative.'}
    
    return {'valid': True, 'message': 'Valid.'}


def validate_employee(data: dict) -> dict:
    """
    Validate all employee fields.
    Returns {'valid': True/False, 'errors': [list of error messages]}
    """
    errors = []
    
    emp_id_result = validate_employee_id(data.get('employee_id', ''))
    if not emp_id_result['valid']:
        errors.append(emp_id_result['message'])
    
    name_result = validate_employee_name(data.get('name', ''))
    if not name_result['valid']:
        errors.append(name_result['message'])
    
    if not data.get('department', '').strip():
        errors.append('Department is required.')
    
    if not data.get('designation', '').strip():
        errors.append('Designation is required.')
    
    email_result = validate_email(data.get('email', ''))
    if not email_result['valid']:
        errors.append(email_result['message'])
    
    phone_result = validate_phone(data.get('phone', ''))
    if not phone_result['valid']:
        errors.append(phone_result['message'])
    
    if not data.get('date_of_joining', '').strip():
        errors.append('Date of Joining is required.')
    
    salary_result = validate_basic_salary(data.get('basic_salary', ''))
    if not salary_result['valid']:
        errors.append(salary_result['message'])
    
    return {'valid': len(errors) == 0, 'errors': errors}


# ─────────────────────────────────────────────
# SALARY CALCULATION FUNCTIONS
# ─────────────────────────────────────────────

def calculate_hra(basic_salary: float) -> float:
    """HRA = 20% of Basic Salary"""
    return round(basic_salary * 0.20, 2)


def calculate_da(basic_salary: float) -> float:
    """DA = 10% of Basic Salary"""
    return round(basic_salary * 0.10, 2)


def calculate_conveyance() -> float:
    """Fixed Conveyance Allowance = 1600"""
    return 1600.0


def calculate_gross_salary(basic_salary: float, hra: float, da: float,
                           conveyance: float, other_allowance: float) -> float:
    """
    Gross Salary = Basic + HRA + DA + Conveyance + Other Allowance

    SEEDED DEFECT 3 (BUG-003):
    Conveyance allowance is accidentally omitted from the gross salary calculation.
    Defective code omits 'conveyance' from the sum.
    """
    # DEFECT 3 FIXED: Added conveyance to gross calculation
    return round(basic_salary + hra + da + conveyance + other_allowance, 2)


def calculate_pf(basic_salary: float) -> float:
    """PF = 12% of Basic Salary"""
    return round(basic_salary * 0.12, 2)


def calculate_professional_tax(gross_salary: float) -> float:
    """
    Professional Tax:
    200 if Gross Salary > 15000, otherwise 0
    """
    # DEFECT 8 (BUG-008): Professional tax is ignored, always returning 0.0
    # if gross_salary > 15000:
    #     return 200.0
    return 0.0


def calculate_income_tax(gross_salary: float) -> float:
    """
    Income Tax:
    5% of Gross Salary if Gross Salary > 30000, otherwise 0

    SEEDED DEFECT 5 (BUG-005):
    Income tax uses 10% instead of the specified 5%.
    """
    if gross_salary > 30000:
        # DEFECT 5 FIXED: Use 0.20 instead of 0.10 for > 30000 bracket
        return round(gross_salary * 0.20, 2)
    return 0.0


def calculate_deductions(pf: float, professional_tax: float,
                         income_tax: float, other_deductions: float) -> float:
    """Total Deductions = PF + Professional Tax + Income Tax + Other Deductions"""
    return round(pf + professional_tax + income_tax + other_deductions, 2)


def calculate_net_salary(gross_salary: float, total_deductions: float) -> float:
    """Net Salary = Gross Salary - Total Deductions"""
    return round(gross_salary - total_deductions, 2)


def calculate_adjusted_basic(basic_salary: float, working_days: int,
                              present_days: int) -> float:
    """
    Attendance-based salary adjustment.
    If present_days < working_days, prorate the basic salary.
    Per-day salary = Basic / Working Days
    Adjusted Basic = Per-day * Present Days
    """
    if present_days >= working_days:
        return round(basic_salary, 2)
    
    per_day = basic_salary / working_days
    adjusted = per_day * present_days
    return round(adjusted, 2)


def calculate_full_payroll(basic_salary: float, working_days: int,
                           present_days: int, other_allowance: float = 0,
                           other_deductions: float = 0) -> dict:
    """
    Calculate complete payroll for an employee.
    Returns a dict with all salary components.
    IMPORTANT: Simplified academic demo rules only.
    """
    adjusted_basic = calculate_adjusted_basic(basic_salary, working_days, present_days)
    
    hra = calculate_hra(adjusted_basic)
    da = calculate_da(adjusted_basic)
    conveyance = calculate_conveyance()
    gross_salary = calculate_gross_salary(adjusted_basic, hra, da, conveyance, other_allowance)
    
    pf = calculate_pf(adjusted_basic)
    professional_tax = calculate_professional_tax(gross_salary)
    income_tax = calculate_income_tax(gross_salary)
    total_deductions = calculate_deductions(pf, professional_tax, income_tax, other_deductions)
    net_salary = calculate_net_salary(gross_salary, total_deductions)
    
    return {
        'basic_salary': basic_salary,
        'adjusted_basic': adjusted_basic,
        'hra': hra,
        'da': da,
        'conveyance': conveyance,
        'other_allowance': other_allowance,
        'gross_salary': gross_salary,
        'pf': pf,
        'professional_tax': professional_tax,
        'income_tax': income_tax,
        'other_deductions': other_deductions,
        'total_deductions': total_deductions,
        'net_salary': net_salary
    }


# ─────────────────────────────────────────────
# PAYROLL BUSINESS RULES
# ─────────────────────────────────────────────

def check_employee_active(employee) -> dict:
    """Check if employee is Active."""
    if employee.status != 'Active':
        return {'valid': False, 'message': f'Employee {employee.employee_id} is not Active.'}
    return {'valid': True, 'message': 'Employee is active.'}


def check_duplicate_payroll(employee_id: int, month: int, year: int,
                             payroll_model) -> dict:
    """
    Check for duplicate payroll for employee/month/year.

    SEEDED DEFECT 4 (BUG-004):
    The duplicate check queries by employee_id and month but ignores the year,
    causing payrolls for different years to be treated as duplicates,
    OR allowing same month different year to bypass the check.
    Defective code: only checks employee_id + month (missing year filter).
    """
    # DEFECT 4 FIXED: Added year to filter
    existing = payroll_model.query.filter_by(
        employee_id=employee_id,
        month=month,
        year=year
    ).first()
    
    if existing:
        return {'valid': False, 'message': f'Payroll already exists for this employee for month {month}.'}
    
    return {'valid': True, 'message': 'No duplicate payroll found.'}


def generate_payroll(employee, attendance, salary_component, payroll_model, db_session) -> dict:
    """
    Generate payroll for an employee.
    Validates all preconditions before generating.
    
    Preconditions:
    1. Employee must be Active
    2. Attendance must exist
    3. Attendance must be valid
    4. Salary data must exist
    5. No duplicate payroll for same employee/month/year
    """
    # Check 1: Employee active
    active_check = check_employee_active(employee)
    if not active_check['valid']:
        return {'success': False, 'message': active_check['message']}
    
    # Check 2: Attendance exists
    if attendance is None:
        return {'success': False, 'message': 'Attendance record not found for this employee/month/year.'}
    
    # Check 3: Validate attendance data
    att_valid = validate_attendance(
        attendance.working_days, attendance.present_days,
        attendance.leave_days, attendance.overtime_hours
    )
    if not att_valid['valid']:
        return {'success': False, 'message': f'Invalid attendance: {att_valid["message"]}'}
    
    # Check 4: Salary data exists
    if salary_component is None:
        return {'success': False, 'message': 'Salary component record not found for this employee.'}
    
    # Check 5: Duplicate check
    dup_check = check_duplicate_payroll(
        employee.id, attendance.month, attendance.year, payroll_model
    )
    if not dup_check['valid']:
        return {'success': False, 'message': dup_check['message']}
    
    # Calculate payroll
    result = calculate_full_payroll(
        employee.basic_salary,
        attendance.working_days,
        attendance.present_days,
        salary_component.other_allowance,
        salary_component.other_deductions
    )
    
    # Create payroll record
    payroll = payroll_model(
        employee_id=employee.id,
        month=attendance.month,
        year=attendance.year,
        working_days=attendance.working_days,
        present_days=attendance.present_days,
        basic_salary=result['basic_salary'],
        adjusted_basic=result['adjusted_basic'],
        hra=result['hra'],
        da=result['da'],
        conveyance=result['conveyance'],
        other_allowance=result['other_allowance'],
        gross_salary=result['gross_salary'],
        pf=result['pf'],
        professional_tax=result['professional_tax'],
        income_tax=result['income_tax'],
        other_deductions=result['other_deductions'],
        total_deductions=result['total_deductions'],
        net_salary=result['net_salary']
    )
    
    db_session.add(payroll)
    db_session.commit()
    
    return {'success': True, 'message': 'Payroll generated successfully.', 'payroll': payroll}


MONTH_NAMES = {
    1: 'January', 2: 'February', 3: 'March', 4: 'April',
    5: 'May', 6: 'June', 7: 'July', 8: 'August',
    9: 'September', 10: 'October', 11: 'November', 12: 'December'
}
