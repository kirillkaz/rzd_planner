from dash_extensions.enrich import html

from rzd_planner.layouts.components.header import render_user_header


def render_user_routes_page() -> html.Div:
    """Функция для отрисовки страницы маршрутов станций"""
    return html.Div(
        children=[
            render_user_header(),
        ],
    )
