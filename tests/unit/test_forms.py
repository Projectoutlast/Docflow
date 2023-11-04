def test_register_forms(test_client):
    """
    GET CompanyRegisterForm and EmployeeRegisterForm
    THEN check that the form work correctly
    """
    from web_app.blueprints.registration.forms import CompanyRegisterForm, EmployeeRegisterForm

    new_company = CompanyRegisterForm(first_name="Tomas", last_name="Andersen", name_of_company="Tylip",
                                      email="tl@bk.ru", tax_id_number=111111, password="123456", confirm="123456")
    assert new_company.validation() is True

    exist_company = CompanyRegisterForm(first_name="Tomas", last_name="Andersen", name_of_company="Tylip",
                                        email="tl@bk.ru", tax_id_number=111111, password="123456", confirm="12356")
    assert exist_company.validation() is False

    exist_company = CompanyRegisterForm(name="", email="", tax_id_number="")
    assert exist_company.validation() is False

    new_employee = EmployeeRegisterForm(first_name="Mikhail", last_name="Arbuzov", email="arbuz@gmail.com",
                                        company_tax_id_number=453380, password="123456", confirm="123456")
    assert new_employee.validation() is True

    invalid_data = EmployeeRegisterForm(first_name="", last_name="", email="",
                                        company_tax_id_number=None, password="", confirm="")
    assert invalid_data.validation() is False

    exists_user = EmployeeRegisterForm(first_name="Mikhail", last_name="Arbuzov", email="john@example.com",
                                       company_tax_id_number=453380, password="123456", confirm="123456")
    assert exists_user.validation() is False
