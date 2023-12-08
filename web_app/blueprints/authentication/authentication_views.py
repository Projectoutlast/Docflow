import sqlalchemy.exc

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user, login_required

from web_app import db
from web_app.models import Employee
from web_app.blueprints.authentication.form import LoginForm, ResetPasswordForm
from web_app.utils.utilities import generate_new_password
from web_app.utils.send_email import send_email


blueprint = Blueprint('login', __name__)


@blueprint.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        if current_user.is_confirmed:
            return redirect(url_for("work.home_workspace"))
        return redirect(url_for("work.unconfirmed_workspace"))

    form = LoginForm(request.form)
    if form.validate_on_submit():
        employee = Employee.query.filter(Employee.email == form.email.data).first()
        if employee and employee.check_password_hash(form.password.data):
            login_user(employee)
            return redirect(url_for("work.unconfirmed_workspace"))
        else:
            flash("Invalid email or password", "danger")
            return render_template("login.html", form=form), 401
    return render_template("login.html", form=form)


@blueprint.route("/login/reset-pwd", methods=["GET", "POST"])
def reset_user_password():
    form = ResetPasswordForm(request.form)
    if form.validate_on_submit():
        employee = Employee.query.filter(Employee.email == form.email.data).first()
        if employee:
            new_password = generate_new_password()
            employee.generate_password_hash(new_password)

            db.session.commit()

            url = url_for("login.login", _external=True)
            render_html = render_template("reset_password_email.html", password=new_password, url=url)
            subject = "Reset password"
            send_email(employee.email, subject, render_html)

            flash("The message with the new password was sent to your address.", "success")
            return redirect(url_for("login.login"))
        flash(f"The user with {form.email.data} address was not found.", "warning")
    return render_template("reset_password.html", form=form)


@blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You were logged out.", "success")
    return redirect(url_for("login.login"))
