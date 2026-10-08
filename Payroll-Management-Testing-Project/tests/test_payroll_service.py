import pytest
import uuid
from datetime import datetime
from app import create_app
from app.models.models import db, Employee, Attendance, SalaryComponent, Payroll
from app.services.payroll_service import (
    validate_employee_id, validate_employee_name, validate_email, validate_phone,
    validate_basic_salary, validate_attendance, validate_other_allowance, validate_other_deductions,
    validate_employee,
    calculate_hra, calculate_da, calculate_conveyance, calculate_gross_salary,
    calculate_pf, calculate_professional_tax, calculate_income_tax,
    calculate_deductions, calculate_net_salary, calculate_adjusted_basic,
    calculate_full_payroll, check_employee_active, check_duplicate_payroll,
    generate_payroll
)

@pytest.fixture
def app():
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def sample_employee(app):
    unique_id = f"EMP{str(uuid.uuid4().int)[:3]}"
    emp = Employee(
        employee_id=unique_id,
        name="Test Employee",
        department="IT",
        designation="Developer",
        email="test@test.com",
        phone="1234567890",
        date_of_joining=datetime.strptime("2020-01-01", "%Y-%m-%d").date(),
        basic_salary=50000.0,
        status="Active"
    )
    db.session.add(emp)
    db.session.commit()
    return emp

# 1
def test_validate_employee_id_valid():
    assert validate_employee_id("EMP123")['valid'] == True

# 2
def test_validate_employee_id_invalid():
    assert validate_employee_id("123")['valid'] == False
    assert validate_employee_id("")['valid'] == False

# 3
def test_validate_employee_name_valid():
    assert validate_employee_name("John Doe")['valid'] == True

# 4
def test_validate_employee_name_invalid():
    assert validate_employee_name("J")['valid'] == False
    assert validate_employee_name("A"*51)['valid'] == False
    assert validate_employee_name("123")['valid'] == False
    assert validate_employee_name("")['valid'] == False

# 5
def test_validate_email():
    assert validate_email("test@example.com")['valid'] == True
    assert validate_email("invalid")['valid'] == False

# 6
def test_validate_phone():
    assert validate_phone("9876543210")['valid'] == True
    assert validate_phone("123")['valid'] == False

# 7
def test_validate_other_allowance():
    assert validate_other_allowance(100)['valid'] == True
    assert validate_other_allowance(-1)['valid'] == False

# 8
def test_validate_other_deductions():
    assert validate_other_deductions(100)['valid'] == True
    assert validate_other_deductions(-1)['valid'] == False

# 9
def test_validate_employee_payload_valid():
    valid_data = {
        'employee_id': 'EMP123', 'name': 'John Doe', 'department': 'IT',
        'designation': 'Dev', 'email': 'john@test.com', 'phone': '9876543210',
        'date_of_joining': '2020-01-01', 'basic_salary': 50000
    }
    assert validate_employee(valid_data)['valid'] == True

# 10
def test_validate_employee_payload_invalid():
    res = validate_employee({})
    assert res['valid'] == False
    assert len(res['errors']) > 0

# 11
def test_validate_basic_salary():
    assert validate_basic_salary(10000)['valid'] == True
    assert validate_basic_salary(9999)['valid'] == False
    assert validate_basic_salary(500000)['valid'] == True
    assert validate_basic_salary(500001)['valid'] == False

# 12
def test_validate_attendance_valid():
    assert validate_attendance(30, 25, 5, 0)['valid'] == True

# 13
def test_validate_attendance_invalid():
    assert validate_attendance(31, 20, 20, 0)['valid'] == False
    assert validate_attendance(30, 31, 0, 0)['valid'] == False
    assert validate_attendance(0, 0, 0, 0)['valid'] == False

# 14
def test_calculate_basic_components():
    assert calculate_hra(10000) == 2000
    assert calculate_da(10000) == 1000
    assert calculate_conveyance() == 1600.0
    assert calculate_pf(10000) == 1200

# 15
def test_calculate_gross_salary():
    # 50000 + 10000 + 5000 + 2000 + 1000 = 68000
    assert calculate_gross_salary(50000, 10000, 5000, 2000, 1000) == 68000

# 16
def test_calculate_taxes():
    assert calculate_professional_tax(20000) == 200
    assert calculate_professional_tax(10000) == 0
    assert calculate_income_tax(20000) == 0.0
    assert calculate_income_tax(40000) == 8000.0
    assert calculate_income_tax(120000) == 24000.0

# 17
def test_calculate_net_and_adjusted_salary():
    assert calculate_deductions(1000, 200, 500, 100) == 1800
    assert calculate_net_salary(50000, 5000) == 45000
    assert calculate_adjusted_basic(30000, 30, 30) == 30000
    assert calculate_adjusted_basic(30000, 30, 15) == 15000

# 18
def test_calculate_full_payroll():
    full = calculate_full_payroll(30000, 30, 30, 0, 0)
    assert 'net_salary' in full
    assert full['basic_salary'] == 30000

# 19
def test_check_employee_active(sample_employee):
    assert check_employee_active(sample_employee)['valid'] == True
    sample_employee.status = "Inactive"
    assert check_employee_active(sample_employee)['valid'] == False

# 20
def test_check_duplicate_payroll(app, sample_employee):
    p = Payroll(employee_id=sample_employee.id, month=1, year=2026, working_days=30, present_days=30,
                basic_salary=50000, adjusted_basic=50000, hra=10000, da=5000, conveyance=1600,
                other_allowance=0, gross_salary=65000, pf=6000, professional_tax=200, income_tax=0,
                other_deductions=0, total_deductions=6200, net_salary=58800)
    db.session.add(p)
    db.session.commit()
    assert check_duplicate_payroll(sample_employee.id, 1, 2026, Payroll)['valid'] == False
    assert check_duplicate_payroll(sample_employee.id, 1, 2027, Payroll)['valid'] == True
    assert check_duplicate_payroll(sample_employee.id, 2, 2026, Payroll)['valid'] == True

# 21
def test_generate_payroll_success(app, sample_employee):
    att = Attendance(employee_id=sample_employee.id, month=5, year=2026, working_days=30, present_days=25, leave_days=5, overtime_hours=0)
    sc = SalaryComponent(employee_id=sample_employee.id, other_allowance=1000, other_deductions=500)
    db.session.add_all([att, sc])
    db.session.commit()
    
    res = generate_payroll(sample_employee, att, sc, Payroll, db.session)
    assert res['success'] == True

# 22
def test_generate_payroll_invalid_attendance(app, sample_employee):
    att = Attendance(employee_id=sample_employee.id, month=6, year=2026, working_days=30, present_days=40, leave_days=5, overtime_hours=0)
    sc = SalaryComponent(employee_id=sample_employee.id, other_allowance=1000, other_deductions=500)
    db.session.add_all([att, sc])
    db.session.commit()
    
    res = generate_payroll(sample_employee, att, sc, Payroll, db.session)
    assert res['success'] == False

# 23
def test_generate_payroll_missing_data(app, sample_employee):
    res = generate_payroll(sample_employee, None, None, Payroll, db.session)
    assert res['success'] == False
    
    att = Attendance(employee_id=sample_employee.id, month=7, year=2026, working_days=30, present_days=25, leave_days=5, overtime_hours=0)
    res = generate_payroll(sample_employee, att, None, Payroll, db.session)
    assert res['success'] == False
