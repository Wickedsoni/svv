import pytest
import uuid
from app import create_app
from app.models.models import db, User, Employee, Attendance, SalaryComponent, Payroll, AuditLog

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

# 24
def test_user_creation(app):
    user = User(username="admin_test", password_hash="hashed_password", full_name="Admin User")
    db.session.add(user)
    db.session.commit()
    assert user.id is not None
    assert user.username == "admin_test"
    assert user.password_hash == "hashed_password"

# 25
def test_employee_creation(app):
    unique_id = f"EMP{str(uuid.uuid4().int)[:3]}"
    emp = Employee(
        employee_id=unique_id,
        name="John Doe",
        department="HR",
        designation="Manager",
        email="john@example.com",
        phone="9876543210",
        date_of_joining="2020-01-01",
        basic_salary=60000.0,
        status="Active"
    )
    db.session.add(emp)
    db.session.commit()
    assert emp.id is not None
    assert emp.employee_id == unique_id
    assert emp.department == "HR"

# 26
def test_attendance_creation(app):
    emp = Employee(employee_id=f"EMP{str(uuid.uuid4().int)[:3]}", name="Jane Doe", department="IT", designation="Dev", email="jane@test.com", phone="9999999999", date_of_joining="2020-01-01", basic_salary=50000.0)
    db.session.add(emp)
    db.session.commit()
    
    att = Attendance(employee_id=emp.id, month=1, year=2026, working_days=31, present_days=30, leave_days=1, overtime_hours=5)
    db.session.add(att)
    db.session.commit()
    assert att.id is not None
    assert att.month == 1
    assert att.working_days == 31

# 27
def test_salary_component_creation(app):
    emp = Employee(employee_id=f"EMP{str(uuid.uuid4().int)[:3]}", name="Jim Doe", department="IT", designation="Dev", email="jim@test.com", phone="9999999998", date_of_joining="2020-01-01", basic_salary=50000.0)
    db.session.add(emp)
    db.session.commit()
    
    sc = SalaryComponent(employee_id=emp.id, other_allowance=1000, other_deductions=500)
    db.session.add(sc)
    db.session.commit()
    assert sc.id is not None
    assert sc.other_allowance == 1000

# 28
def test_payroll_creation(app):
    emp = Employee(employee_id=f"EMP{str(uuid.uuid4().int)[:3]}", name="Jill Doe", department="IT", designation="Dev", email="jill@test.com", phone="9999999997", date_of_joining="2020-01-01", basic_salary=50000.0)
    db.session.add(emp)
    db.session.commit()
    
    payroll = Payroll(
        employee_id=emp.id, month=2, year=2026, working_days=28, present_days=28,
        basic_salary=50000, adjusted_basic=50000, hra=10000, da=5000, conveyance=1600,
        other_allowance=0, gross_salary=66600, pf=6000, professional_tax=200, income_tax=3330,
        other_deductions=0, total_deductions=9530, net_salary=57070
    )
    db.session.add(payroll)
    db.session.commit()
    assert payroll.id is not None
    assert payroll.net_salary == 57070

# 29
def test_audit_log_creation(app):
    log = AuditLog(action="CREATE_EMPLOYEE", module="Employee", details="Created EMP001")
    db.session.add(log)
    db.session.commit()
    assert log.id is not None
    assert log.action == "CREATE_EMPLOYEE"
