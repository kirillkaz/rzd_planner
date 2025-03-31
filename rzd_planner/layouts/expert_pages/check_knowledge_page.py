from dash_extensions.enrich import html

from rzd_planner.layouts.components.header import render_expert_header
from rzd_planner.layouts.components.table_component import render_table
from rzd_planner.layouts.components.table_header import render_table_header


def render_check_knowledge_page() -> html.Div:
    """Функция для отрисовки страницы проверки базы знаний"""
    _cols_defs = [
        {"name": "", "id": "knowledge_type"},
        {"name": "Описание", "id": "description"},
    ]

    return html.Div(
        children=[
            render_expert_header(),
            html.Div(
                children=[
                    render_table_header(
                        left_childrens=[
                            html.Div(
                                "Таблица маршрутов",
                                className="table-header-title",
                            )
                        ],
                        right_childrens=[],
                    ),
                    render_table(
                        table_id="check-knowledge-table-id",
                        columns_def=_cols_defs,
                        row_selectable=None,
                    ),
                ],
                className="table-block",
            ),
        ],
    )
