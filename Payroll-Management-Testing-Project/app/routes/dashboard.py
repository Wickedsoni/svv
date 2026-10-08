"""Dashboard route"""
from flask import Blueprint, render_template
from flask_login import login_required
from app.models.models import Employee, Payroll
from datetime import datetime

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/dashboard')
@login_required
def index():
    total_employees = Employee.query.count()
    active_employees = Employee.query.filter_by(status='Active').count()
    inactive_employees = Employee.query.filter_by(status='Inactive').count()
    total_payrolls = Payroll.query.count()
    
    now = datetime.now()
    current_month_payrolls = Payroll.query.filter_by(
        month=now.month, year=now.year
    ).all()
    current_month_total = sum(p.net_salary for p in current_month_payrolls)
    
    return render_template(
        'dashboard.html',
        total_employees=total_employees,
        active_employees=active_employees,
        inactive_employees=inactive_employees,
        total_payrolls=total_payrolls,
        current_month_total=current_month_total,
        current_month=now.strftime('%B %Y')
    )
