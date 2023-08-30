import sqlalchemy.exc
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user

from web_app import db
from web_app.models import Company, Employee
from web_app.blueprints.registration.forms import CompanyRegisterForm, EmployeeRegisterForm

blueprint = Blueprint('registration', __name__)


@blueprint.route('/company', methods=['GET', 'POST'])
def registration_company():
    if current_user.is_authenticated:
        return redirect(url_for("login.login"))
    form = CompanyRegisterForm(request.form)
    if form.validate_on_submit():
        try:
            company = Company(company_name=form.name.data,
                              tax_id_number=form.tax_id_number.data,
                              company_email=form.email.data)
            db.session.add(company)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()
            flash("This email or tax Id number is already exist", "danger")
            return render_template('registration/company.html', form=form), 409

        flash("Your company registered. Please confirm your email", "message")
        return redirect(url_for("main.index"))
    return render_template('registration/company.html', form=form)


@blueprint.route('/employee', methods=['GET', 'POST'])
def registration_employee():
    if current_user.is_authenticated:
        return redirect(url_for("login.login"))
    form = EmployeeRegisterForm(request.form)
    if form.validate_on_submit():
        is_company_exist = Company.query.filter(Company.tax_id_number == form.company_tax_id_number.data).first()
        if not is_company_exist:
            flash("This company doesn't not exist.", "message")
            return render_template('registration/employee.html', form=form), 404
        try:
            employee = Employee(company_id=form.company_tax_id_number.data,  # type: ignore
                                first_name=form.first_name.data,  # type: ignore
                                last_name=form.last_name.data,  # type: ignore
                                email=form.email.data,  # type: ignore
                                password=form.password.data)  # type: ignore
            employee.generate_password_hash(employee.password)
            db.session.add(employee)
            db.session.commit()

            flash("Your register complete. Please confirm email!", "success")
            return redirect(url_for("login.login"))
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()
            flash("User with this email is already exist", "danger")
            return render_template('registration/employee.html', form=form), 409
    return render_template('registration/employee.html', form=form)
