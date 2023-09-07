from datetime import date, datetime, time


from flask_wtf import FlaskForm
from wtforms import BooleanField, DateField, SelectField, StringField, SubmitField, TimeField, TextAreaField
from wtforms.validators import DataRequired, Length

from web_app.models import Employee


class NewActivityCall(FlaskForm):

    to_whom = StringField("To whom", validators=[DataRequired(), Length(min=2, max=60)])
    when_date = DateField("Date", validators=[DataRequired()])
    when_time = TimeField("Time", validators=[DataRequired()])
    executor = SelectField("Executor", coerce=int, validators=[DataRequired()])
    myself = BooleanField("Myself")
    submit = SubmitField("Create")


class NewActivityMeeting(FlaskForm):

    with_whom = StringField("With whom", validators=[DataRequired(), Length(min=2, max=60)])
    location = StringField("Location", validators=[DataRequired()])
    when_date = DateField("Date", validators=[DataRequired()])
    when_time = TimeField("Time", validators=[DataRequired()])
    executor = SelectField("Executor", coerce=int, validators=[DataRequired()])
    myself = BooleanField("Myself")
    submit = SubmitField("Create")


class NewActivityTask(FlaskForm):

    subject = StringField("Subject", validators=[DataRequired(), Length(min=2, max=60)])
    describe = TextAreaField("Describe", validators=[DataRequired()])
    when_date = DateField("Date", validators=[DataRequired()])
    when_time = TimeField("Time", validators=[DataRequired()])
    executor = SelectField("Executor", coerce=int, validators=[DataRequired()])
    myself = BooleanField("Myself")
    submit = SubmitField("Create")


def get_all_executors(activity_holder_id: int) -> list[tuple]:

    """Get all employee for exact company for Activities dropdown field Executor"""

    company_id = Employee.query.filter(Employee.id == activity_holder_id).first()
    all_executors = Employee.query.filter(Employee.company_id == company_id.company_id).all()
    result = [(employee.id, f"{employee.first_name} {employee.last_name}") for employee in all_executors]
    return result


def combine_date_time(dt: date, tm: time) -> datetime:

    """Combined date and time from Activity forms to datetime object"""

    return datetime.combine(dt, tm)


def get_executor(form_instance: NewActivityCall | NewActivityMeeting | NewActivityTask) -> int:

    """Get executor from forms and return value for db"""

    return form_instance.myself.data if form_instance.myself.data else form_instance.executor.data
