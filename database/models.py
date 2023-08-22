from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from flask_login import UserMixin

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


password_hasher = PasswordHasher()


class Base(DeclarativeBase):
    pass


class Company(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_name: Mapped[str] = mapped_column(nullable=False)
    tax_id_number: Mapped[int] = mapped_column(unique=True, nullable=False)
    company_email: Mapped[str] = mapped_column(unique=True, nullable=False)
    is_confirm: Mapped[bool] = mapped_column(nullable=False, default=False)

    department: Mapped["Department"] = relationship(back_populates="company")
    employee: Mapped["Employee"] = relationship(back_populates="company")

    def __repr__(self):
        return f"<Company name {self.company_name}, email {self.company_email}>"


class Department(Base):
    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"))
    head_of_department_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=True, default=None)
    department_name: Mapped[str] = mapped_column(nullable=False)
    describe_function: Mapped[str] = mapped_column(nullable=True)

    company: Mapped["Company"] = relationship(back_populates="department", foreign_keys=[company_id])
    employee: Mapped["Employee"] = relationship(foreign_keys=[head_of_department_id])


class Employee(UserMixin, Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"))
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"), nullable=True, default=None)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    position: Mapped[str] = mapped_column(nullable=False, default="manager")
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    company: Mapped["Company"] = relationship(back_populates="employee", foreign_keys=[company_id])
    department: Mapped["Department"] = relationship(foreign_keys=[department_id])

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
