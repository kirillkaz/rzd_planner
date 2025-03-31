from dash_extensions.enrich import html

from rzd_planner.layouts.components.header import render_expert_header


def render_routes_page() -> html.Div:
    """Функция для отрисовки страницы маршрутов"""
    return html.Div(
        children=[
            render_expert_header(),
        ],
    )
