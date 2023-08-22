from decouple import config

from flask import Flask
from flask_login import LoginManager

from blueprints.main.main_views import blueprint as main_blueprint
from blueprints.registration.registration_views import blueprint as registration_blueprint
from blueprints.authentication.authentication_views import blueprint as authentication_blueprint
from blueprints.work.work_views import blueprint as work_blueprint

from database.engine import session
from database.models import Employee


def create_app():

    app = Flask(__name__)

    app.config.from_object(config("APP_SETTINGS"))

    login_manager = LoginManager()
    login_manager.init_app(app)

    app.register_blueprint(main_blueprint)
    app.register_blueprint(registration_blueprint)
    app.register_blueprint(authentication_blueprint)
    app.register_blueprint(work_blueprint)

    login_manager.login_view = "login"

    @login_manager.user_loader
    def load_user(user_id):
        return session.query(Employee).where(Employee.id == int(user_id)).first()

    return app


if __name__ == '__main__':
    create_app().run(debug=True, port=4242)
