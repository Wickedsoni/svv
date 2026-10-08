"""
Database seed data for Payroll Management System
Team 11 — Academic Demo
"""
from werkzeug.security import generate_password_hash
from datetime import datetime


def seed_database():
    """Seed the database with initial demo data if not already populated."""
    from app import db
    from app.models.models import User, Employee, Attendance, SalaryComponent
    
    # Seed admin user
    if not User.query.filter_by(username='admin').first():
        admin = User(
            username='admin',
            password_hash=generate_password_hash('admin123'),
            full_name='System Administrator',
            role='admin'
        )
        db.session.add(admin)
        db.session.commit()
    
    # Seed 5 demo employees
    if Employee.query.count() == 0:
        employees_data = [
            {
                'employee_id': 'EMP001',
                'name': 'Rajesh Kumar',
                'department': 'Engineering',
                'designation': 'Software Engineer',
                'email': 'rajesh.kumar@company.com',
                'phone': '9876543210',
                'date_of_joining': '2022-01-15',
                'basic_salary': 45000.0,
                'status': 'Active'
            },
            {
                'employee_id': 'EMP002',
                'name': 'Priya Sharma',
                'department': 'Human Resources',
                'designation': 'HR Executive',
                'email': 'priya.sharma@company.com',
                'phone': '8765432109',
                'date_of_joining': '2021-06-01',
                'basic_salary': 38000.0,
                'status': 'Active'
            },
            {
                'employee_id': 'EMP003',
                'name': 'Suresh Patel',
                'department': 'Finance',
                'designation': 'Accounts Manager',
                'email': 'suresh.patel@company.com',
                'phone': '7654321098',
                'date_of_joining': '2020-03-20',
                'basic_salary': 55000.0,
                'status': 'Active'
            },
            {
                'employee_id': 'EMP004',
                'name': 'Anita Singh',
                'department': 'Marketing',
                'designation': 'Marketing Executive',
                'email': 'anita.singh@company.com',
                'phone': '6543210987',
                'date_of_joining': '2023-07-10',
                'basic_salary': 32000.0,
                'status': 'Active'
            },
            {
                'employee_id': 'EMP005',
                'name': 'Vijay Mehta',
                'department': 'Operations',
                'designation': 'Operations Lead',
                'email': 'vijay.mehta@company.com',
                'phone': '9012345678',
                'date_of_joining': '2019-11-05',
                'basic_salary': 62000.0,
                'status': 'Inactive'
            }
        ]
        
        for emp_data in employees_data:
            employee = Employee(**emp_data)
            db.session.add(employee)
        
        db.session.commit()
        
        # Seed salary components for all employees
        for emp in Employee.query.all():
            sc = SalaryComponent(
                employee_id=emp.id,
                other_allowance=500.0,
                other_deductions=0.0
            )
            db.session.add(sc)
        
        # Seed attendance for Sep 2026 for first 4 employees
        attendance_data = [
            {'emp_id': 'EMP001', 'month': 9, 'year': 2026, 'working_days': 26, 'present_days': 26, 'leave_days': 0, 'overtime_hours': 5},
            {'emp_id': 'EMP002', 'month': 9, 'year': 2026, 'working_days': 26, 'present_days': 24, 'leave_days': 2, 'overtime_hours': 0},
            {'emp_id': 'EMP003', 'month': 9, 'year': 2026, 'working_days': 26, 'present_days': 26, 'leave_days': 0, 'overtime_hours': 10},
            {'emp_id': 'EMP004', 'month': 9, 'year': 2026, 'working_days': 26, 'present_days': 20, 'leave_days': 6, 'overtime_hours': 0},
        ]
        
        for att_data in attendance_data:
            emp = Employee.query.filter_by(employee_id=att_data['emp_id']).first()
            if emp:
                att = Attendance(
                    employee_id=emp.id,
                    month=att_data['month'],
                    year=att_data['year'],
                    working_days=att_data['working_days'],
                    present_days=att_data['present_days'],
                    leave_days=att_data['leave_days'],
                    overtime_hours=att_data['overtime_hours']
                )
                db.session.add(att)
        
        db.session.commit()
