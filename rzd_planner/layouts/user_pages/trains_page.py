import dash_bootstrap_components as dbc
from dash_extensions.enrich import html

from rzd_planner.layouts.components.header import render_user_header
from rzd_planner.layouts.components.table_component import render_table
from rzd_planner.layouts.components.table_header import render_table_header


def render_trains_page() -> html.Div:
    """Функция для отрисовки страницы поездов"""
    _cols_defs = [
        {"name": "Номер поезда", "id": "train_number"},
        {"name": "Тип поезда", "id": "train_type"},
        {"name": "Скорость поезда", "id": "train_speed"},
        {"name": "Дальность следования", "id": "travel_distance"},
    ]

    return html.Div(
        children=[
            render_user_header(),
            html.Div(
                children=[
                    render_table_header(
                        left_childrens=[
                            html.Div(
                                "Таблица поездов",
                                className="table-header-title",
                            )
                        ],
                        right_childrens=[
                            dbc.Button(
                                children="Добавить поезд",
                                color="secondary",
                                id="trains-add-btn-id",
                            ),
                            dbc.Button(
                                children="Удалить поезда",
                                color="secondary",
                                id="trains-delete-btn-id",
                            ),
                        ],
                    ),
                    render_table(table_id="trains-table-id", columns_def=_cols_defs),
                ],
                className="table-block",
            ),
        ],
    )
