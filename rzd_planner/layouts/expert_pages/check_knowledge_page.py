from dash_extensions.enrich import html

from rzd_planner.layouts.components.header import render_expert_header


def render_check_knowledge_page() -> html.Div:
    """Функция для отрисовки страницы проверки базы знаний"""
    return html.Div(
        children=[
            render_expert_header(),
        ],
    )
