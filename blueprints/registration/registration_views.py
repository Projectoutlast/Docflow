import sqlalchemy.exc
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user

from blueprints.registration.forms import CompanyRegisterForm, EmployeeRegisterForm
from database.engine import db_session
from database.models import Company, Employee

blueprint = Blueprint('registration', __name__)


@blueprint.route('/company', methods=['GET', 'POST'])
def registration_company():
    if current_user.is_authenticated:
        flash("You are already registered.", "info")
        return redirect(url_for("login.login"))
    form = CompanyRegisterForm(request.form)
    if form.validate_on_submit():
        try:
            company = Company(company_name=form.name.data,
                              tax_id_number=form.tax_id_number.data,
                              company_email=form.email.data)
            db_session.add(company)
            db_session.commit()
        except sqlalchemy.exc.IntegrityError:
            db_session.rollback()
            flash("This email or tax Id number is already exist", "danger")
            return render_template('registration/company.html', form=form)

        flash("Your company registered. Please confirm your email", "message")
        return redirect(url_for("main.index"))
    return render_template('registration/company.html', form=form)


@blueprint.route('/employee', methods=['GET', 'POST'])
def registration_employee():
    if current_user.is_authenticated:
        flash("You are already registered.", "info")
        return redirect(url_for("login.login"))
    form = EmployeeRegisterForm(request.form)
    if form.validate_on_submit():
        is_company_exist = db_session.query(Company).where(Company.tax_id_number == form.company_tax_id_number.data).first()
        if not is_company_exist:
            flash("This company doesn't not exist.", "message")
            return render_template('registration/employee.html', form=form)
        try:
            employee = Employee(company_id=form.company_tax_id_number.data,
                                first_name=form.first_name.data,
                                last_name=form.last_name.data,
                                email=form.email.data,
                                password=form.password.data)
            employee.generate_password_hash(employee.password)
            db_session.add(employee)
            db_session.commit()

            flash("Your register complete. Please confirm email!", "success")
            return redirect(url_for("login.login"))
        except sqlalchemy.exc.IntegrityError:
            db_session.rollback()
            flash("User with this email is already exist", "danger")
            return render_template('registration/employee.html', form=form)
    return render_template('registration/employee.html', form=form)
