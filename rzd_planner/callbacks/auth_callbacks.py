from typing import TypedDict

from dash.exceptions import PreventUpdate
from dash_extensions.enrich import Input, Output, State, ctx, no_update

from rzd_planner.app import app
from rzd_planner.config import UserRoles
from rzd_planner.services.auth_service import AuthService
from rzd_planner.services.dao.users_dao import UserDAO


class AuthCallbackReturn(TypedDict):
    """Структура возвращаемая колбэком auth_callback"""

    url: str


@app.callback(
    output=dict(url=Output("redirect", "pathname")),
    inputs=dict(
        _=Input("login-confirm-button-id", "n_clicks"),
        username=State("login-field-id", "value"),
        password=State("password-field-id", "value"),
    ),
    prevent_initial_call=True,
)
def auth_callback(_: int, username: str, password: str) -> AuthCallbackReturn:
    """Колбэк для авторизации пользователя

    Args:
        username (str): Имя пользователя
        password (str): Пароль пользователя

    Returns:
        str: redirect
    """
    if _ is None:
        raise PreventUpdate

    is_authenticated = AuthService().authorize(username=username, pwd=password)

    if is_authenticated:
        with app.server.app_context():
            user_role = UserDAO().get_role_by_username(username)
            if user_role == str(UserRoles.EXPERT):
                return AuthCallbackReturn(url="/train_type")
            else:
                return AuthCallbackReturn(url="/trains")

    return AuthCallbackReturn(url=no_update)
