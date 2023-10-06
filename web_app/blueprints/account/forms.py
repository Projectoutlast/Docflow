from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import EmailField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class EditData(FlaskForm):
    first_name = StringField("First name", validators=[DataRequired()])
    last_name = StringField("Last name", validators=[DataRequired()])
    email = EmailField("Email", validators=[Email()])
    submit = SubmitField("Save changes")


class EditPhoto(FlaskForm):
    photo = FileField("Photo (.jpg or .png format only)", validators=[FileRequired()])
    submit = SubmitField("Update")


class ChangePassword(FlaskForm):
    current_password = PasswordField("Current password", validators=[DataRequired()])
    new_password = PasswordField("New password", validators=[DataRequired(), Length(min=6, max=50)])
    confirm_new_password = PasswordField("Confirm new password", validators=[DataRequired(),
                                                                             EqualTo("new_password",
                                                                                     message="Passwords must match")])
    submit = SubmitField("Update")
