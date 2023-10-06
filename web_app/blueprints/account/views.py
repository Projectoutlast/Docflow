import pathlib

import sqlalchemy.exc

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from config import basedir
from web_app import db
from web_app.blueprints.account.forms import ChangePassword, EditData, EditPhoto
from web_app.models import Company, Employee
from web_app.utils.utilities import get_path_to_profile_photo


blueprint = Blueprint("settings", __name__)


@blueprint.route("/user", methods=["GET"])
@login_required
def user_settings():
    employee = Employee.query.filter(Employee.id == current_user.id).first()
    company = Company.query.filter(Company.id == employee.company_id).first()
    return render_template("account/employee_data.html", employee=employee, company=company)


@blueprint.route("/user/edit", methods=["GET", "POSt"])
@login_required
def user_edit_information():
    employee = Employee.query.filter(Employee.id == current_user.id).first()
    company = Company.query.filter(Company.id == employee.company_id).first()
    form_data = EditData()
    form_photo = EditPhoto()

    return render_template("account/edit_profile.html", employee=employee, company=company,
                           form_data=form_data, form_photo=form_photo)


@blueprint.route("/user/edit/data", methods=["POST"])
@login_required
def user_edit_data_process():
    employee = Employee.query.filter(Employee.id == current_user.id).first()
    form = EditData()

    if form.validate_on_submit():
        employee.first_name = form.first_name.data
        employee.last_name = form.last_name.data
        employee.email = form.email.data
        try:
            db.session.commit()
            flash("Profile successfully updated!", "success")
            return redirect(url_for("settings.user_settings"))
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()
            flash("Invalid data was passed, try again!", "danger")

    return redirect(url_for("settings.user_edit_information"))


@blueprint.route("/user/edit/photo", methods=["POST"])
@login_required
def user_edit_photo_process():
    employee = Employee.query.filter(Employee.id == current_user.id).first()
    form = EditPhoto()

    if form.validate_on_submit():
        file = form.photo.data
        filename = secure_filename(file.filename)
        file_path = get_path_to_profile_photo(
            f"{basedir}/web_app/static/profile_photos/{current_user.id}") + f"/{filename}"
        file.save(file_path)

        employee.profile_photo = file_path

        try:
            db.session.commit()
            flash("Photo successfully updated!", "success")
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()
            flash("Invalid data was passed, try again!", "danger")

    return redirect(url_for("settings.user_edit_information"))


@blueprint.route("/user/change/password", methods=["GET", "POST"])
@login_required
def user_change_password():
    form = ChangePassword()
    if form.validate_on_submit():
        pass
    return render_template("account/change_password.html", form=form)
