"""Payroll generation and payslip routes"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.models.models import Employee, Attendance, SalaryComponent, Payroll
from app.services.payroll_service import generate_payroll, MONTH_NAMES

payroll_bp = Blueprint('payroll', __name__)

MONTHS = list(MONTH_NAMES.items())


@payroll_bp.route('/payroll')
@login_required
def index():
    payrolls = db.session.query(Payroll, Employee).join(
        Employee, Payroll.employee_id == Employee.id
    ).order_by(Payroll.year.desc(), Payroll.month.desc()).all()
    return render_template('payroll/index.html', payrolls=payrolls, month_names=MONTH_NAMES)


@payroll_bp.route('/payroll/generate', methods=['GET', 'POST'])
@login_required
def generate():
    employees = Employee.query.filter_by(status='Active').all()
    
    if request.method == 'POST':
        emp_db_id = request.form.get('employee_id', '')
        month = request.form.get('month', '')
        year = request.form.get('year', '')
        
        if not emp_db_id or not month or not year:
            flash('Employee, Month, and Year are required.', 'danger')
            return render_template('payroll/generate.html', employees=employees, months=MONTHS)
        
        employee = Employee.query.get(int(emp_db_id))
        if not employee:
            flash('Employee not found.', 'danger')
            return render_template('payroll/generate.html', employees=employees, months=MONTHS)
        
        attendance = Attendance.query.filter_by(
            employee_id=employee.id, month=int(month), year=int(year)
        ).first()
        
        salary_component = SalaryComponent.query.filter_by(employee_id=employee.id).first()
        
        result = generate_payroll(employee, attendance, salary_component, Payroll, db.session)
        
        if result['success']:
            flash(f'Payroll generated successfully for {employee.name} — {MONTH_NAMES[int(month)]} {year}!', 'success')
            return redirect(url_for('payroll.index'))
        else:
            flash(result['message'], 'danger')
            return render_template('payroll/generate.html', employees=employees, months=MONTHS,
                                   form_data=request.form)
    
    return render_template('payroll/generate.html', employees=employees, months=MONTHS,
                           form_data={})


@payroll_bp.route('/payroll/<int:pay_id>/payslip')
@login_required
def payslip(pay_id):
    payroll = Payroll.query.get_or_404(pay_id)
    employee = Employee.query.get(payroll.employee_id)
    month_name = MONTH_NAMES.get(payroll.month, str(payroll.month))
    return render_template('payroll/payslip.html', payroll=payroll, employee=employee,
                           month_name=month_name)


@payroll_bp.route('/payslips')
@login_required
def payslips():
    payrolls = db.session.query(Payroll, Employee).join(
        Employee, Payroll.employee_id == Employee.id
    ).order_by(Payroll.year.desc(), Payroll.month.desc()).all()
    return render_template('payroll/payslips.html', payrolls=payrolls, month_names=MONTH_NAMES)
