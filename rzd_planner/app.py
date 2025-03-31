import dash_bootstrap_components as dbc
import flask_migrate
from dash_extensions.enrich import DashProxy, MultiplexerTransform
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate

from rzd_planner.config import config
from rzd_planner.models import db


def init_app() -> DashProxy:
    """Функция для создания инстанса приложения"""
    server = Flask(__name__)
    server.config.from_object(config)
    db.init_app(server)
    Migrate().init_app(server, db)
    with server.app_context():
        flask_migrate.upgrade(directory="migrations/")

    return DashProxy(
        transforms=[MultiplexerTransform()],
        external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],
        server=server,
        assets_folder="./assets",
        suppress_callback_exceptions=True,
    )


app = init_app()

login_manager = LoginManager()
login_manager.init_app(app.server)
login_manager.login_view = "/login"
