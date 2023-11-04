import datetime

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from flask_login import UserMixin

from config import Config
from web_app.enums import ActivityStatus, Roles, TypeOfActivity
from web_app import db

password_hasher = PasswordHasher()


class Company(db.Model):
    __tablename__ = "companies"

    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String, nullable=False)
    tax_id_number = db.Column(db.Integer, unique=True, nullable=False)
    company_email = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return f"<Company name {self.company_name}, email {self.company_email}>"


class Department(db.Model):
    __tablename__ = "departments"

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"))
    head_of_department_id = db.Column(db.Integer, db.ForeignKey("employees.id"), nullable=True, default=None)
    department_name = db.Column(db.String, nullable=False)
    describe_function = db.Column(db.String, nullable=True)


class Employee(db.Model, UserMixin):
    __tablename__ = "employees"

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"))
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"), nullable=True, default=None)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    roles = db.Column(db.Enum(Roles), default=Roles.MANAGER, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    is_confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    profile_photo = db.Column(db.String, default=Config.DEFAULT_AVATAR_PATH)

    def __repr__(self):
        return f"<User Id={self.id}, company-{self.company_id}>"

    def generate_password_hash(self, password: str) -> None:
        self.password = password_hasher.hash(password)

    def check_password_hash(self, password: str) -> bool:
        try:
            password_hasher.verify(self.password, password)
            return True
        except VerifyMismatchError:
            return False


class CallActivity(db.Model):
    __tablename__ = "call_activities"

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False)
    type_of = db.Column(db.Enum(TypeOfActivity), default=TypeOfActivity.CALL, nullable=False)
    to_whom = db.Column(db.String, nullable=False)
    activity_holder = db.Column(db.Integer, db.ForeignKey("employees.id"), nullable=False)
    activity_holder_name = db.Column(db.String, nullable=False)
    executor = db.Column(db.Integer, db.ForeignKey("employees.id"), nullable=False)
    executor_name = db.Column(db.String, nullable=False)
    appointed = db.Column(db.DateTime, default=datetime.datetime.now())
    finish_until = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum(ActivityStatus), default=ActivityStatus.IN_PROGRESS, nullable=False)

    def __repr__(self):
        return f"<Id={self.id}, activity_holder={self.activity_holder}>"


class MeetingActivity(db.Model):
    __tablename__ = "meeting_activities"

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False)
    type_of = db.Column(db.Enum(TypeOfActivity), default=TypeOfActivity.MEETING, nullable=False)
    with_whom = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    activity_holder = db.Column(db.Integer, db.ForeignKey("employees.id"), nullable=False)
    activity_holder_name = db.Column(db.String, nullable=False)
    executor = db.Column(db.Integer, db.ForeignKey("employees.id"), nullable=False)
    executor_name = db.Column(db.String, nullable=False)
    appointed = db.Column(db.DateTime, default=datetime.datetime.now())
    finish_until = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum(ActivityStatus), default=ActivityStatus.IN_PROGRESS, nullable=False)

    def __repr__(self):
        return f"<Id={self.id}, activity_holder={self.activity_holder}>"


class TaskActivity(db.Model):
    __tablename__ = "task_activities"

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False)
    type_of = db.Column(db.Enum(TypeOfActivity), default=TypeOfActivity.TASK, nullable=False)
    subject = db.Column(db.String, nullable=False)
    describe = db.Column(db.String, nullable=False)
    activity_holder = db.Column(db.Integer, db.ForeignKey("employees.id"), nullable=False)
    activity_holder_name = db.Column(db.String, nullable=False)
    executor = db.Column(db.Integer, db.ForeignKey("employees.id"), nullable=False)
    executor_name = db.Column(db.String, nullable=False)
    appointed = db.Column(db.DateTime, default=datetime.datetime.now())
    finish_until = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum(ActivityStatus), default=ActivityStatus.IN_PROGRESS, nullable=False)

    def __repr__(self):
        return f"<Id={self.id}, activity_holder={self.activity_holder}>"
