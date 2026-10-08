"""Reports routes"""
from flask import Blueprint, render_template, request
from flask_login import login_required
from app import db
from app.models.models import Employee, Payroll
from app.services.payroll_service import MONTH_NAMES

reports_bp = Blueprint('reports', __name__)


@reports_bp.route('/reports')
@login_required
def index():
    return render_template('reports/index.html')


@reports_bp.route('/reports/employees')
@login_required
def employee_report():
    status_filter = request.args.get('status', '')
    dept_filter = request.args.get('department', '').strip()
    
    query = Employee.query
    if status_filter:
        query = query.filter_by(status=status_filter)
    if dept_filter:
        query = query.filter(Employee.department.ilike(f'%{dept_filter}%'))
    
    employees = query.all()
    departments = db.session.query(Employee.department).distinct().all()
    departments = [d[0] for d in departments]
    
    return render_template('reports/employee_report.html',
                           employees=employees, departments=departments,
                           status_filter=status_filter, dept_filter=dept_filter)


@reports_bp.route('/reports/payroll')
@login_required
def payroll_report():
    month_filter = request.args.get('month', '')
    year_filter = request.args.get('year', '')
    
    query = db.session.query(Payroll, Employee).join(
        Employee, Payroll.employee_id == Employee.id
    )
    
    if month_filter:
        query = query.filter(Payroll.month == int(month_filter))
    if year_filter:
        query = query.filter(Payroll.year == int(year_filter))
    
    payrolls = query.order_by(Payroll.year.desc(), Payroll.month.desc()).all()
    total_gross = sum(p.gross_salary for p, e in payrolls)
    total_deductions = sum(p.total_deductions for p, e in payrolls)
    total_net = sum(p.net_salary for p, e in payrolls)
    
    return render_template('reports/payroll_report.html',
                           payrolls=payrolls, month_names=MONTH_NAMES,
                           total_gross=total_gross, total_deductions=total_deductions,
                           total_net=total_net, month_filter=month_filter, year_filter=year_filter)


@reports_bp.route('/reports/monthly-summary')
@login_required
def monthly_summary():
    # Summarize payroll by month/year
    results = db.session.query(
        Payroll.year, Payroll.month,
        db.func.count(Payroll.id).label('count'),
        db.func.sum(Payroll.gross_salary).label('total_gross'),
        db.func.sum(Payroll.net_salary).label('total_net')
    ).group_by(Payroll.year, Payroll.month).order_by(
        Payroll.year.desc(), Payroll.month.desc()
    ).all()
    
    return render_template('reports/monthly_summary.html',
                           results=results, month_names=MONTH_NAMES)
