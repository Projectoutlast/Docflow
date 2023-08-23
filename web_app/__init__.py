from decouple import config

from flask import Flask
from flask_login import LoginManager
from web_app.database.db import db


def create_app() -> Flask:

    app = Flask(__name__)

    app.config.from_object(config("APP_SETTINGS"))

    db.init_app(app)
    with app.app_context():
        from web_app.database.models import Company, Department, Employee
        db.create_all()

    login_manager = LoginManager()
    login_manager.init_app(app)

    from web_app.blueprints.main.main_views import blueprint as main_blueprint
    from web_app.blueprints.registration.registration_views import blueprint as registration_blueprint
    from web_app.blueprints.authentication.authentication_views import blueprint as authentication_blueprint
    from web_app.blueprints.work.work_views import blueprint as work_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(registration_blueprint)
    app.register_blueprint(authentication_blueprint)
    app.register_blueprint(work_blueprint)

    login_manager.login_view = "login"

    from web_app.database.models import Employee

    @login_manager.user_loader
    def load_user(user_id):
        return Employee.query.filter(Employee.id == int(user_id)).first()

    return app


flask_app = create_app()
