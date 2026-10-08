"""Salary Components routes"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.models.models import Employee, SalaryComponent
from app.services.payroll_service import (
    validate_other_allowance, validate_other_deductions,
    calculate_hra, calculate_da, calculate_conveyance,
    calculate_gross_salary, calculate_pf, calculate_professional_tax,
    calculate_income_tax, calculate_deductions, calculate_net_salary
)

salary_bp = Blueprint('salary', __name__)


@salary_bp.route('/salary')
@login_required
def index():
    components = db.session.query(SalaryComponent, Employee).join(
        Employee, SalaryComponent.employee_id == Employee.id
    ).all()
    return render_template('salary/index.html', components=components)


@salary_bp.route('/salary/<int:sc_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(sc_id):
    sc = SalaryComponent.query.get_or_404(sc_id)
    employee = Employee.query.get(sc.employee_id)
    
    if request.method == 'POST':
        other_allowance = request.form.get('other_allowance', '0')
        other_deductions = request.form.get('other_deductions', '0')
        
        result_a = validate_other_allowance(other_allowance)
        result_d = validate_other_deductions(other_deductions)
        
        if not result_a['valid']:
            flash(result_a['message'], 'danger')
            return render_template('salary/edit.html', sc=sc, employee=employee)
        
        if not result_d['valid']:
            flash(result_d['message'], 'danger')
            return render_template('salary/edit.html', sc=sc, employee=employee)
        
        sc.other_allowance = float(other_allowance)
        sc.other_deductions = float(other_deductions)
        db.session.commit()
        flash('Salary components updated successfully!', 'success')
        return redirect(url_for('salary.view', sc_id=sc.id))
    
    return render_template('salary/edit.html', sc=sc, employee=employee)


@salary_bp.route('/salary/<int:sc_id>')
@login_required
def view(sc_id):
    sc = SalaryComponent.query.get_or_404(sc_id)
    employee = Employee.query.get(sc.employee_id)
    
    basic = employee.basic_salary
    hra = calculate_hra(basic)
    da = calculate_da(basic)
    conveyance = calculate_conveyance()
    gross = calculate_gross_salary(basic, hra, da, conveyance, sc.other_allowance)
    pf = calculate_pf(basic)
    prof_tax = calculate_professional_tax(gross)
    inc_tax = calculate_income_tax(gross)
    total_ded = calculate_deductions(pf, prof_tax, inc_tax, sc.other_deductions)
    net = calculate_net_salary(gross, total_ded)
    
    preview = {
        'basic': basic, 'hra': hra, 'da': da, 'conveyance': conveyance,
        'other_allowance': sc.other_allowance, 'gross': gross,
        'pf': pf, 'prof_tax': prof_tax, 'inc_tax': inc_tax,
        'other_deductions': sc.other_deductions, 'total_ded': total_ded, 'net': net
    }
    
    return render_template('salary/view.html', sc=sc, employee=employee, preview=preview)
