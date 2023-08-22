from flask_wtf import FlaskForm
from wtforms import EmailField, IntegerField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from database.engine import session
from database.models import Company, Employee


class CompanyRegisterForm(FlaskForm):
    name = StringField("Company name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(), Email(message=None), Length(min=6, max=40)])
    tax_id_number = IntegerField("Tax identification number", validators=[DataRequired()])
    submit = SubmitField("Register")

    def validation(self) -> bool:
        initial_validation = super(CompanyRegisterForm, self).validate()
        if not initial_validation:
            return False
        company = session.query(Company).where(Company.company_email == self.email.data).first()
        if company:
            self.email.errors.append("Email already registered")
            return False
        return True


class EmployeeRegisterForm(FlaskForm):
    first_name = StringField("First name", validators=[DataRequired(), Length(max=90)])
    last_name = StringField("Last name", validators=[DataRequired(), Length(max=90)])
    email = EmailField("Email", validators=[DataRequired(), Email(message=None), Length(min=6, max=40)])
    company_tax_id_number = IntegerField("Company tax Id number", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=50)])
    confirm = PasswordField("Repeat password", validators=[DataRequired(), EqualTo("password",
                                                                                   message="Passwords must match")])
    submit = SubmitField("Register")

    def validation(self) -> bool:
        initial_validation = super(EmployeeRegisterForm, self).validate()
        if not initial_validation:
            return False
        employee = session.query(Employee).where(Employee.email == self.email.data).first()
        if employee:
            self.email.errors.append("Email already registered")
            return False
        if self.password.data != self.confirm.data:
            self.email.errors.append("Passwords must match")
            return False
        return True
