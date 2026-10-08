"""
Payroll Management System - Demo Application
Team 11 | Manual Testing Demo Application
IMPORTANT: Simplified payroll calculation rules for academic demonstration only.
"""
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = 'payroll-demo-secret-key-team11'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///payroll.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['WTF_CSRF_ENABLED'] = False
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'warning'
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.employees import employees_bp
    from app.routes.attendance import attendance_bp
    from app.routes.salary import salary_bp
    from app.routes.payroll import payroll_bp
    from app.routes.reports import reports_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(employees_bp)
    app.register_blueprint(attendance_bp)
    app.register_blueprint(salary_bp)
    app.register_blueprint(payroll_bp)
    app.register_blueprint(reports_bp)
    
    # Create tables
    with app.app_context():
        db.create_all()
        from app.database.seed import seed_database
        seed_database()
    
    return app
