import pytest
from app import create_app, db
from app.models.models import Employee, SalaryComponent, Attendance, Payroll
from app.services.payroll_service import generate_payroll
import datetime

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

def test_integration_1_login_to_dashboard(client):
    """Integration Test 1: Test Login Flow to Dashboard"""
    response = client.post('/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=True)
    assert b'Dashboard' in response.data

def test_integration_2_employee_creation_db(client):
    """Integration Test 2: Route -> Service -> DB (Employee Creation)"""
    client.post('/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=True)
    client.post('/employees/add', data={
        'employee_id': 'EMP999', 'name': 'Integration Test', 'department': 'IT', 
        'designation': 'Dev', 'email': 'test@test.com', 'phone': '9876543210', 
        'date_of_joining': '2026-01-01', 'basic_salary': '50000'
    }, follow_redirects=True)
    
    emp = Employee.query.filter_by(employee_id='EMP999').first()
    assert emp is not None
    assert emp.name == 'Integration Test'

def test_integration_3_salary_auto_creation(client):
    """Integration Test 3: Employee Creation Auto-creates Salary Component"""
    client.post('/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=True)
    client.post('/employees/add', data={
        'employee_id': 'EMP998', 'name': 'Salary Test', 'department': 'IT', 
        'designation': 'Dev', 'email': 't@t.com', 'phone': '9876543210', 
        'date_of_joining': '2026-01-01', 'basic_salary': '50000'
    }, follow_redirects=True)
    
    emp = Employee.query.filter_by(employee_id='EMP998').first()
    salary_comp = SalaryComponent.query.filter_by(employee_id=emp.id).first()
    assert salary_comp is not None
    assert salary_comp.other_allowance == 0.0

def test_integration_4_attendance_record_db(client):
    """Integration Test 4: Route -> DB (Attendance Creation)"""
    client.post('/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=True)
    # Add employee first
    client.post('/employees/add', data={
        'employee_id': 'EMP997', 'name': 'Att Test', 'department': 'IT', 
        'designation': 'Dev', 'email': 'a@a.com', 'phone': '9876543210', 
        'date_of_joining': '2026-01-01', 'basic_salary': '50000'
    }, follow_redirects=True)
    emp = Employee.query.filter_by(employee_id='EMP997').first()
    
    # Record Attendance
    client.post('/attendance/add', data={
        'employee_id': emp.id, 'month': '1', 'year': '2026', 
        'working_days': '30', 'present_days': '30', 'leave_days': '0', 'overtime_hours': '5'
    }, follow_redirects=True)
    
    att = Attendance.query.filter_by(employee_id=emp.id).first()
    assert att is not None
    assert att.present_days == 30

def test_integration_5_payroll_generation_service(client):
    """Integration Test 5: End to End Payroll Generation"""
    client.post('/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=True)
    client.post('/employees/add', data={
        'employee_id': 'EMP996', 'name': 'Pay Test', 'department': 'IT', 
        'designation': 'Dev', 'email': 'p@p.com', 'phone': '9876543210', 
        'date_of_joining': '2026-01-01', 'basic_salary': '50000'
    }, follow_redirects=True)
    emp = Employee.query.filter_by(employee_id='EMP996').first()
    
    client.post('/attendance/add', data={
        'employee_id': emp.id, 'month': '2', 'year': '2026', 
        'working_days': '28', 'present_days': '28', 'leave_days': '0', 'overtime_hours': '0'
    }, follow_redirects=True)
    
    response = client.post('/payroll/generate', data={
        'employee_id': emp.id, 'month': '2', 'year': '2026'
    }, follow_redirects=True)
    
    assert b'Payroll generated successfully' in response.data
    payroll = Payroll.query.filter_by(employee_id=emp.id).first()
    assert payroll is not None

def test_integration_6_payroll_missing_attendance(client):
    """Integration Test 6: Payroll Service rejects missing attendance"""
    client.post('/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=True)
    client.post('/employees/add', data={
        'employee_id': 'EMP995', 'name': 'Miss Test', 'department': 'IT', 
        'designation': 'Dev', 'email': 'm@m.com', 'phone': '9876543210', 
        'date_of_joining': '2026-01-01', 'basic_salary': '50000'
    }, follow_redirects=True)
    emp = Employee.query.filter_by(employee_id='EMP995').first()
    
    response = client.post('/payroll/generate', data={
        'employee_id': emp.id, 'month': '3', 'year': '2026'
    }, follow_redirects=True)
    assert b'Attendance record not found' in response.data

def test_integration_7_duplicate_payroll_prevention(client):
    """Integration Test 7: Route -> Service Prevent Duplicate Payroll"""
    client.post('/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=True)
    client.post('/employees/add', data={
        'employee_id': 'EMP994', 'name': 'Dup Test', 'department': 'IT', 
        'designation': 'Dev', 'email': 'd@d.com', 'phone': '9876543210', 
        'date_of_joining': '2026-01-01', 'basic_salary': '50000'
    }, follow_redirects=True)
    emp = Employee.query.filter_by(employee_id='EMP994').first()
    
    client.post('/attendance/add', data={
        'employee_id': emp.id, 'month': '4', 'year': '2026', 
        'working_days': '30', 'present_days': '30', 'leave_days': '0', 'overtime_hours': '0'
    })
    
    client.post('/payroll/generate', data={'employee_id': emp.id, 'month': '4', 'year': '2026'})
    response = client.post('/payroll/generate', data={'employee_id': emp.id, 'month': '4', 'year': '2026'}, follow_redirects=True)
    assert b'already exists' in response.data

def test_integration_8_employee_deletion_cascade(client):
    """Integration Test 8: DB Cascade constraints (Employee deletion removes SalaryComponent)"""
    client.post('/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=True)
    client.post('/employees/add', data={
        'employee_id': 'EMP993', 'name': 'Del Test', 'department': 'IT', 
        'designation': 'Dev', 'email': 'del@d.com', 'phone': '9876543210', 
        'date_of_joining': '2026-01-01', 'basic_salary': '50000'
    }, follow_redirects=True)
    
    emp = Employee.query.filter_by(employee_id='EMP993').first()
    db.session.delete(emp)
    db.session.commit()
    
    sc = SalaryComponent.query.filter_by(employee_id=emp.id).first()
    assert sc is None # Foreign key cascade ensures this is deleted

def test_integration_9_reports_generation_route(client):
    """Integration Test 9: Reports Route fetches Payrolls from DB"""
    client.post('/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=True)
    response = client.get('/reports')
    assert response.status_code == 200
    assert b'Payroll Report' in response.data

def test_integration_10_auth_middleware(client):
    """Integration Test 10: Auth Middleware blocks unauthenticated access to endpoints"""
    response = client.get('/dashboard')
    assert response.status_code == 302 # Redirect to login
    response2 = client.get('/employees/add')
    assert response2.status_code == 302
