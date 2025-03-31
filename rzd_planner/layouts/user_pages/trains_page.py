from dash_extensions.enrich import html

from rzd_planner.layouts.components.header import render_user_header


def render_trains_page() -> html.Div:
    """Функция для отрисовки страницы поездов"""
    return html.Div(
        children=[
            render_user_header(),
        ],
    )
