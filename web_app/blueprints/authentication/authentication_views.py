from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user, login_required

from web_app.models import Employee
from web_app.blueprints.authentication.form import LoginForm


blueprint = Blueprint('login', __name__)


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("work.home_workspace"))
    form = LoginForm(request.form)
    if form.validate_on_submit():
        employee = Employee.query.filter(Employee.email == form.email.data).first()
        if employee and employee.check_password_hash(form.password.data):
            login_user(employee)
            return redirect(url_for("work.home_workspace"))
        else:
            flash("Invalid email or password", "danger")
            return render_template("login.html", form=form), 401
    return render_template("login.html", form=form)


@blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You were logged out.", "success")
    return redirect(url_for("login.login"))
