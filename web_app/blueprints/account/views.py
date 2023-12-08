import sqlalchemy.exc

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from config import Config
from web_app import db
from web_app.blueprints.account.forms import ChangePassword, EditData, EditPhoto
from web_app.models import Company, Employee
from web_app.utils.send_email import generate_and_send_confirmation_token
from web_app.utils.utilities import check_extension_file, get_path_to_profile_photo


blueprint = Blueprint("settings", __name__)


@blueprint.route("/user", methods=["GET"])
@login_required
def user_settings():
    employee = Employee.query.filter(Employee.id == current_user.id).first()
    company = Company.query.filter(Company.id == employee.company_id).first()
    return render_template("account/employee_data.html", employee=employee, company=company)


@blueprint.route("/user/edit", methods=["GET", "POST"])
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
    previous_email = employee.email
    form = EditData()

    if form.validate_on_submit():
        employee.first_name = form.first_name.data
        employee.last_name = form.last_name.data
        if employee.email != form.email.data:
            employee.email = form.email.data
            employee.is_confirmed = False
            generate_and_send_confirmation_token(employee.email)

        if previous_email != form.email.data:

            flash("Profile successfully updated"
                  "and we sent confirmation email on the new address. Please, confirm it", "success")
        else:
            flash("Profile successfully updated!", "success")
        db.session.commit()
        return redirect(url_for("settings.user_settings"))

    return redirect(url_for("settings.user_edit_information"))


@blueprint.route("/user/edit/photo", methods=["POST"])
@login_required
def user_edit_photo_process():
    employee = Employee.query.filter(Employee.id == current_user.id).first()
    form = EditPhoto()

    if form.validate_on_submit():
        file = form.photo.data
        filename = secure_filename(file.filename)

        if not check_extension_file(filename):
            flash("Invalid file format", "warning")
            return redirect(request.referrer)

        file_path = get_path_to_profile_photo(f"{Config.PROFILE_PHOTO_FOLDER_PATH}{current_user.id}") + f"/{filename}"
        file.save(file_path)
        employee.profile_photo = file_path

        db.session.commit()
        flash("Photo successfully updated!", "success")
    return redirect(url_for("settings.user_edit_information"))


@blueprint.route("/user/change/password", methods=["GET", "POST"])
@login_required
def user_change_password():
    form = ChangePassword()
    if form.validate_on_submit():
        employee = Employee.query.filter(Employee.id == current_user.id).first()
        if employee and employee.check_password_hash(form.current_password.data):
            employee.generate_password_hash(form.new_password.data)
            db.session.commit()
            flash("Password successfully updated!", "success")
            return redirect(url_for("settings.user_settings"))
        flash("Incorrect current password", "warning")
    return render_template("account/change_password.html", form=form)
