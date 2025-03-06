import dash_bootstrap_components as dbc
from dash_extensions.enrich import DashProxy, MultiplexerTransform
from flask import Flask


def init_app() -> DashProxy:
    """Функция для создания инстанса приложения"""
    server = Flask(__name__)
    return DashProxy(
        transforms=[MultiplexerTransform()],
        external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],
        server=server,
        assets_folder="./assets",
        suppress_callback_exceptions=True,
    )


app = init_app()
