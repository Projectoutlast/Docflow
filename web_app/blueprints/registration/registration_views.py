import datetime

import sqlalchemy.exc
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from web_app import db
from web_app.blueprints.registration.forms import CompanyRegisterForm, EmployeeRegisterForm
from web_app.enums import Roles
from web_app.models import Company, Employee
from web_app.utils.send_email import send_email
from web_app.utils.token import confirm_token, generate_token
from web_app.utils.utilities import email_confirm

blueprint = Blueprint('registration', __name__)


@blueprint.route('/company', methods=['GET', 'POST'])
def registration_company():
    if current_user.is_authenticated:
        return redirect(url_for("login.login"))
    form = CompanyRegisterForm(request.form)
    if form.validate_on_submit():
        try:
            company = Company(company_name=form.name_of_company.data,
                              tax_id_number=form.tax_id_number.data,
                              company_email=form.email.data)
            employee = Employee(company_id=company.id,  # type: ignore
                                first_name=form.first_name.data,  # type: ignore
                                last_name=form.last_name.data,  # type: ignore
                                roles=Roles.HEAD_OF_COMPANY,  # type: ignore
                                email=form.email.data,  # type: ignore
                                password=form.password.data)  # type: ignore
            employee.generate_password_hash(employee.password)
            db.session.add_all([company, employee])
            db.session.commit()

            token = generate_token(employee.email)
            confirm_url = url_for("registration.confirm_email", token=token, _external=True)
            html = render_template("confirm_email.html", confirm_url=confirm_url)
            subject = "Please confirm your email"
            send_email(employee.email, subject, html)

        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()
            flash("This email or tax Id number is already exist", "danger")
            return render_template('registration/company.html', form=form), 409

        flash("Your company registered. Please confirm your email", "message")
        return redirect(url_for("login.login"))
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

            token = generate_token(employee.email)
            confirm_url = url_for("registration.confirm_email", token=token, _external=True)
            html = render_template("confirm_email.html", confirm_url=confirm_url)
            subject = "Please confirm your email"
            send_email(employee.email, subject, html)

            flash("Your register complete. Please confirm email!", "success")
            return redirect(url_for("login.login"))
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()
            flash("User with this email is already exist", "danger")
            return render_template('registration/employee.html', form=form), 409
    return render_template('registration/employee.html', form=form)


@blueprint.route("/confirm/<token>")
@login_required
def confirm_email(token: str):
    if current_user.is_confirmed:
        flash("Account already confirmed.", "success")
        return redirect(url_for("work.home_workspace"))
    email = confirm_token(token)
    employee = Employee.query.filter(Employee.id == current_user.id).first_or_404()
    if employee.email == email:
        employee.is_confirmed = True
        employee.confirmed_on = datetime.datetime.now()
        db.session.add(employee)
        db.session.commit()
        flash("You have confirmed your account! Thanks", "success")
    else:
        flash("The confirmation link is invalid or has expired.", "danger")
    return redirect(url_for("work.home_workspace"))


@blueprint.route("/resend")
@login_required
def resend_confirmation():
    token = generate_token(current_user.email)
    confirm_url = url_for("registration.confirm_email", token=token, _external=True)
    html = render_template("confirm_email.html", confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(current_user.email, subject, html)
    flash("A new confirmation email has been sent.", "success")
    return redirect(url_for("work.unconfirmed_workspace"))
