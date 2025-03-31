import dash_bootstrap_components as dbc
from dash_extensions.enrich import html

from rzd_planner.layouts.components.header import render_user_header
from rzd_planner.layouts.components.table_component import render_table
from rzd_planner.layouts.components.table_header import render_table_header


def render_user_routes_page() -> html.Div:
    """Функция для отрисовки страницы маршрутов станций"""
    _cols_defs = [
        {"name": "Маршрут поездки", "id": "route"},
    ]

    return html.Div(
        children=[
            render_user_header(),
            html.Div(
                children=[
                    render_table_header(
                        left_childrens=[
                            html.Div(
                                "Таблица маршрутов поездок",
                                className="table-header-title",
                            )
                        ],
                        right_childrens=[
                            dbc.Button(
                                children="Добавить маршрут",
                                color="secondary",
                                id="routes-user-add-btn-id",
                            ),
                            dbc.Button(
                                children="Удалить маршруты",
                                color="secondary",
                                id="routes-user-delete-btn-id",
                            ),
                        ],
                    ),
                    render_table(
                        table_id="routes-user-table-id", columns_def=_cols_defs
                    ),
                ],
                className="table-block",
            ),
        ],
    )
