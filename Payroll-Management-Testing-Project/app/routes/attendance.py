"""Attendance management routes"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.models.models import Employee, Attendance
from app.services.payroll_service import validate_attendance

attendance_bp = Blueprint('attendance', __name__)

MONTHS = [
    (1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'),
    (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'),
    (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')
]


@attendance_bp.route('/attendance')
@login_required
def index():
    attendances = db.session.query(Attendance, Employee).join(
        Employee, Attendance.employee_id == Employee.id
    ).all()
    return render_template('attendance/index.html', attendances=attendances, months=MONTHS)


@attendance_bp.route('/attendance/add', methods=['GET', 'POST'])
@login_required
def add():
    employees = Employee.query.filter_by(status='Active').all()
    
    if request.method == 'POST':
        emp_id = request.form.get('employee_id', '')
        month = request.form.get('month', '')
        year = request.form.get('year', '')
        working_days = request.form.get('working_days', '')
        present_days = request.form.get('present_days', '')
        leave_days = request.form.get('leave_days', '')
        overtime_hours = request.form.get('overtime_hours', '0')
        
        # Validate fields
        errors = []
        if not emp_id:
            errors.append('Employee is required.')
        if not month:
            errors.append('Month is required.')
        if not year:
            errors.append('Year is required.')
        
        if not errors:
            att_result = validate_attendance(working_days, present_days, leave_days, overtime_hours)
            if not att_result['valid']:
                errors.append(att_result['message'])
        
        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('attendance/add.html', employees=employees, months=MONTHS,
                                   form_data=request.form)
        
        # Check duplicate attendance
        employee = Employee.query.get(int(emp_id))
        if not employee:
            flash('Employee not found.', 'danger')
            return render_template('attendance/add.html', employees=employees, months=MONTHS,
                                   form_data=request.form)
        
        existing = Attendance.query.filter_by(
            employee_id=employee.id, month=int(month), year=int(year)
        ).first()
        
        if existing:
            flash(f'Attendance already exists for {employee.name} for {month}/{year}.', 'danger')
            return render_template('attendance/add.html', employees=employees, months=MONTHS,
                                   form_data=request.form)
        
        try:
            att = Attendance(
                employee_id=employee.id,
                month=int(month),
                year=int(year),
                working_days=int(working_days),
                present_days=int(present_days),
                leave_days=int(leave_days),
                overtime_hours=float(overtime_hours)
            )
            db.session.add(att)
            db.session.commit()
            flash('Attendance recorded successfully!', 'success')
            return redirect(url_for('attendance.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error recording attendance: {str(e)}', 'danger')
    
    return render_template('attendance/add.html', employees=employees, months=MONTHS,
                           form_data={})


@attendance_bp.route('/attendance/<int:att_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(att_id):
    attendance = Attendance.query.get_or_404(att_id)
    employees = Employee.query.filter_by(status='Active').all()
    
    if request.method == 'POST':
        working_days = request.form.get('working_days', '')
        present_days = request.form.get('present_days', '')
        leave_days = request.form.get('leave_days', '')
        overtime_hours = request.form.get('overtime_hours', '0')
        
        att_result = validate_attendance(working_days, present_days, leave_days, overtime_hours)
        if not att_result['valid']:
            flash(att_result['message'], 'danger')
            return render_template('attendance/edit.html', attendance=attendance,
                                   employees=employees, months=MONTHS)
        
        try:
            attendance.working_days = int(working_days)
            attendance.present_days = int(present_days)
            attendance.leave_days = int(leave_days)
            attendance.overtime_hours = float(overtime_hours)
            db.session.commit()
            flash('Attendance updated successfully!', 'success')
            return redirect(url_for('attendance.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating attendance: {str(e)}', 'danger')
    
    return render_template('attendance/edit.html', attendance=attendance,
                           employees=employees, months=MONTHS)
