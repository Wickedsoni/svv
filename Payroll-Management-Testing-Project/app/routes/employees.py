"""Employee management routes"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from app import db
from app.models.models import Employee
from app.services.payroll_service import validate_employee

employees_bp = Blueprint('employees', __name__)


@employees_bp.route('/employees')
@login_required
def index():
    search = request.args.get('search', '').strip()
    if search:
        employees = Employee.query.filter(
            (Employee.employee_id.ilike(f'%{search}%')) |
            (Employee.name.ilike(f'%{search}%')) |
            (Employee.department.ilike(f'%{search}%'))
        ).all()
    else:
        employees = Employee.query.all()
    return render_template('employees/index.html', employees=employees, search=search)


@employees_bp.route('/employees/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        data = {
            'employee_id': request.form.get('employee_id', '').strip(),
            'name': request.form.get('name', '').strip(),
            'department': request.form.get('department', '').strip(),
            'designation': request.form.get('designation', '').strip(),
            'email': request.form.get('email', '').strip(),
            'phone': request.form.get('phone', '').strip(),
            'date_of_joining': request.form.get('date_of_joining', '').strip(),
            'basic_salary': request.form.get('basic_salary', '').strip(),
        }
        
        # Validate
        result = validate_employee(data)
        if not result['valid']:
            for error in result['errors']:
                flash(error, 'danger')
            return render_template('employees/add.html', form_data=data)
        
        # Check duplicate employee ID
        existing = Employee.query.filter_by(employee_id=data['employee_id']).first()
        if existing:
            flash(f'Employee ID {data["employee_id"]} already exists.', 'danger')
            return render_template('employees/add.html', form_data=data)
        
        try:
            employee = Employee(
                employee_id=data['employee_id'],
                name=data['name'],
                department=data['department'],
                designation=data['designation'],
                email=data['email'],
                phone=data['phone'],
                date_of_joining=data['date_of_joining'],
                basic_salary=float(data['basic_salary']),
                status='Active'
            )
            db.session.add(employee)
            db.session.commit()
            
            # Create default salary component
            from app.models.models import SalaryComponent
            sc = SalaryComponent(employee_id=employee.id, other_allowance=0, other_deductions=0)
            db.session.add(sc)
            db.session.commit()
            
            flash(f'Employee {data["employee_id"]} — {data["name"]} added successfully!', 'success')
            return redirect(url_for('employees.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding employee: {str(e)}', 'danger')
    
    return render_template('employees/add.html', form_data={})


@employees_bp.route('/employees/<int:emp_id>')
@login_required
def view(emp_id):
    employee = Employee.query.get_or_404(emp_id)
    return render_template('employees/view.html', employee=employee)


@employees_bp.route('/employees/<int:emp_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(emp_id):
    employee = Employee.query.get_or_404(emp_id)
    
    if request.method == 'POST':
        data = {
            'employee_id': employee.employee_id,  # ID not editable
            'name': request.form.get('name', '').strip(),
            'department': request.form.get('department', '').strip(),
            'designation': request.form.get('designation', '').strip(),
            'email': request.form.get('email', '').strip(),
            'phone': request.form.get('phone', '').strip(),
            'date_of_joining': request.form.get('date_of_joining', '').strip(),
            'basic_salary': request.form.get('basic_salary', '').strip(),
        }
        
        result = validate_employee(data)
        if not result['valid']:
            for error in result['errors']:
                flash(error, 'danger')
            return render_template('employees/edit.html', employee=employee, form_data=data)
        
        try:
            employee.name = data['name']
            employee.department = data['department']
            employee.designation = data['designation']
            employee.email = data['email']
            employee.phone = data['phone']
            employee.date_of_joining = data['date_of_joining']
            employee.basic_salary = float(data['basic_salary'])
            db.session.commit()
            flash(f'Employee {employee.employee_id} updated successfully!', 'success')
            return redirect(url_for('employees.view', emp_id=emp_id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating employee: {str(e)}', 'danger')
    
    return render_template('employees/edit.html', employee=employee, form_data={})


@employees_bp.route('/employees/<int:emp_id>/toggle-status', methods=['POST'])
@login_required
def toggle_status(emp_id):
    employee = Employee.query.get_or_404(emp_id)
    old_status = employee.status
    employee.status = 'Inactive' if employee.status == 'Active' else 'Active'
    db.session.commit()
    flash(f'Employee {employee.employee_id} status changed from {old_status} to {employee.status}.', 'info')
    return redirect(url_for('employees.view', emp_id=emp_id))
