from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from flask_login import UserMixin

from web_app import db

password_hasher = PasswordHasher()


class Company(db.Model):
    __tablename__ = "companies"

    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String, nullable=False)
    tax_id_number = db.Column(db.Integer, unique=True, nullable=False)
    company_email = db.Column(db.String, unique=True, nullable=False)
    is_confirm = db.Column(db.Boolean, nullable=False, default=False)

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
    position = db.Column(db.String, nullable=False, default="manager")
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

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
