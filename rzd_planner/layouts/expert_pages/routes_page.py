import dash_bootstrap_components as dbc
from dash_extensions.enrich import html

from rzd_planner.layouts.components.header import render_expert_header
from rzd_planner.layouts.components.table_component import render_table
from rzd_planner.layouts.components.table_header import render_table_header


def render_routes_page() -> html.Div:
    """Функция для отрисовки страницы маршрутов"""
    _cols_defs = [
        {"name": "Станция отправления", "id": "start_station"},
        {"name": "Станция прибытия", "id": "end_station"},
        {"name": "Дальность маршрута, Км/ч", "id": "route_distance"},
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
                        right_childrens=[
                            dbc.Button(
                                children="Добавить маршрут",
                                color="secondary",
                                id="routes-expert-add-btn-id",
                            ),
                            dbc.Button(
                                children="Удалить маршруты",
                                color="secondary",
                                id="routes-expert-delete-btn-id",
                            ),
                        ],
                    ),
                    render_table(
                        table_id="routes-expert-table-id", columns_def=_cols_defs
                    ),
                ],
                className="table-block",
            ),
        ],
    )
