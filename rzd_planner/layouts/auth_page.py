import dash_bootstrap_components as dbc
from dash_extensions.enrich import html


def render_auth_page() -> html.Div:
    return html.Div(
        children=[
            html.Div(
                children=[
                    dbc.Input(
                        placeholder="Логин",
                        id="login-field-id",
                        className="login-field",
                    ),
                    dbc.Input(
                        placeholder="Пароль",
                        id="password-field-id",
                        className="password-field",
                    ),
                ],
                className="auth-fields-block",
                id="auth-fields-block-id",
            ),
            dbc.Button(
                children="Войти",
                color="primary",
                className="login-confirm-button",
                id="login-confirm-button-id",
            ),
        ],
    )
