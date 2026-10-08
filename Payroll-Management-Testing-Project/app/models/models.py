"""
Database Models for Payroll Management System
Team 11 — Academic Demo
"""
from datetime import datetime
from flask_login import UserMixin
from app import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), default='admin')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Employee(db.Model):
    __tablename__ = 'employees'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    department = db.Column(db.String(50), nullable=False)
    designation = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    date_of_joining = db.Column(db.String(20), nullable=False)
    basic_salary = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(10), default='Active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    attendance_records = db.relationship('Attendance', backref='employee', lazy=True, cascade='all, delete-orphan')
    salary_components = db.relationship('SalaryComponent', backref='employee', lazy=True, cascade='all, delete-orphan')
    payroll_records = db.relationship('Payroll', backref='employee', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Employee {self.employee_id} {self.name}>'


class Attendance(db.Model):
    __tablename__ = 'attendance'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    working_days = db.Column(db.Integer, nullable=False)
    present_days = db.Column(db.Integer, nullable=False)
    leave_days = db.Column(db.Integer, nullable=False)
    overtime_hours = db.Column(db.Float, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Attendance EmpID={self.employee_id} {self.month}/{self.year}>'


class SalaryComponent(db.Model):
    __tablename__ = 'salary_components'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    other_allowance = db.Column(db.Float, default=0)
    other_deductions = db.Column(db.Float, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<SalaryComponent EmpID={self.employee_id}>'


class Payroll(db.Model):
    __tablename__ = 'payroll'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    working_days = db.Column(db.Integer, nullable=False)
    present_days = db.Column(db.Integer, nullable=False)
    basic_salary = db.Column(db.Float, nullable=False)
    adjusted_basic = db.Column(db.Float, nullable=False)
    hra = db.Column(db.Float, nullable=False)
    da = db.Column(db.Float, nullable=False)
    conveyance = db.Column(db.Float, nullable=False)
    other_allowance = db.Column(db.Float, default=0)
    gross_salary = db.Column(db.Float, nullable=False)
    pf = db.Column(db.Float, nullable=False)
    professional_tax = db.Column(db.Float, nullable=False)
    income_tax = db.Column(db.Float, nullable=False)
    other_deductions = db.Column(db.Float, default=0)
    total_deductions = db.Column(db.Float, nullable=False)
    net_salary = db.Column(db.Float, nullable=False)
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Payroll EmpID={self.employee_id} {self.month}/{self.year}>'


class AuditLog(db.Model):
    __tablename__ = 'audit_log'
    
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(100), nullable=False)
    module = db.Column(db.String(50), nullable=False)
    details = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<AuditLog {self.action} {self.timestamp}>'
