import os

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from config import basedir, config


db = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_view = "login"


def create_app(config_name: str) -> Flask:

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    if os.path.exists(basedir + "/docflow.db"):
        os.remove(basedir + "/docflow.db")

    db.init_app(app)
    with app.app_context():
        from web_app.models import CallActivity, Company, Department, Employee
        db.create_all()
        from tests.utils_for_tests import (generate_activities, generate_activities_for_current_user,
                                           generate_new_company, generate_new_employee, generate_overdue_activities)
        generate_new_company()
        generate_new_employee()
        generate_activities()
        generate_activities_for_current_user()
        generate_overdue_activities()

    login_manager.init_app(app)

    from web_app.blueprints.main.main_views import blueprint as main_blueprint
    app.register_blueprint(main_blueprint)

    from web_app.blueprints.registration.registration_views import blueprint as registration_blueprint
    app.register_blueprint(registration_blueprint)

    from web_app.blueprints.authentication.authentication_views import blueprint as authentication_blueprint
    app.register_blueprint(authentication_blueprint)

    from web_app.blueprints.work.activity.views import blueprint as work_blueprint
    app.register_blueprint(work_blueprint)

    from web_app.models import Employee

    @login_manager.user_loader
    def load_user(user_id):
        return Employee.query.filter(Employee.id == int(user_id)).first()

    return app
