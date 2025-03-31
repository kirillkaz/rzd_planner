import dash_bootstrap_components as dbc
from dash_extensions.enrich import html


def render_expert_header() -> dbc.Nav:
    """Функция для прорисовки хеадера эксперта"""
    return dbc.Nav(
        children=[
            dbc.NavItem(dbc.NavLink("Тип поезда", href="/train_type", active=True)),
            dbc.NavItem(dbc.NavLink("Станции", href="/stations")),
            dbc.NavItem(dbc.NavLink("Маршруты", href="/routes_expert")),
            dbc.NavItem(
                dbc.NavLink("Проверка полноты базы знаний", href="/check_knowledge")
            ),
        ],
    )


def render_user_header() -> html.Div:
    """Функция для прорисовки хеадера пользователя"""
    return dbc.Nav(
        children=[
            dbc.NavItem(dbc.NavLink("Поезда", href="/trains", active=True)),
            dbc.NavItem(dbc.NavLink("Маршруты станции", href="/routes_user")),
            dbc.NavItem(dbc.NavLink("Время поездки", href="/travel_times")),
        ],
    )
