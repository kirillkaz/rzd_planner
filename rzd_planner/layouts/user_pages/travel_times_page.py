import dash_bootstrap_components as dbc
from dash_extensions.enrich import html

from rzd_planner.layouts.components.header import render_user_header
from rzd_planner.layouts.components.table_component import render_table
from rzd_planner.layouts.components.table_header import render_table_header


def render_travel_times_page() -> html.Div:
    """Функция для отрисовки страницы времени поездки"""
    _cols_defs = [
        {"name": "Маршрут поездки", "id": "travel_route"},
        {"name": "Время начала поездки", "id": "start_datetime"},
        {"name": "Время конца поездки", "id": "end_datetime"},
    ]

    return html.Div(
        children=[
            render_user_header(),
            html.Div(
                children=[
                    render_table_header(
                        left_childrens=[
                            html.Div(
                                "Таблица времени поездок",
                                className="table-header-title",
                            )
                        ],
                        right_childrens=[
                            dbc.Button(
                                children="Добавить время поездки",
                                color="secondary",
                                id="travel-times-add-btn-id",
                            ),
                            dbc.Button(
                                children="Удалить времена поездок",
                                color="secondary",
                                id="travel-times-delete-btn-id",
                            ),
                        ],
                    ),
                    render_table(
                        table_id="travel-times-table-id", columns_def=_cols_defs
                    ),
                ],
                className="table-block",
            ),
        ],
    )
