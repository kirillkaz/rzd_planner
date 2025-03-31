import dash_bootstrap_components as dbc
from dash_extensions.enrich import html

from rzd_planner.layouts.components.header import render_expert_header
from rzd_planner.layouts.components.table_component import render_table
from rzd_planner.layouts.components.table_header import render_table_header


def render_train_types_page() -> html.Div:
    """Функция для отрисовки типов поездов"""

    _cols_defs = [
        {"name": "Тип поезда", "id": "train_type"},
        {"name": "Скорость", "id": "speed"},
        {"name": "Дальность поездки", "id": "travel_distance"},
    ]

    return html.Div(
        children=[
            render_expert_header(),
            html.Div(
                children=[
                    render_table_header(
                        left_childrens=[
                            html.Div(
                                "Таблица типов поездов",
                                className="table-header-title",
                            )
                        ],
                        right_childrens=[
                            dbc.Button(
                                children="Добавить тип поезда",
                                color="secondary",
                                id="train-types-add-btn-id",
                            ),
                            dbc.Button(
                                children="Удалить типы поездов",
                                color="secondary",
                                id="train-types-delete-btn-id",
                            ),
                        ],
                    ),
                    render_table(
                        table_id="train-types-table-id", columns_def=_cols_defs
                    ),
                ],
                className="table-block",
            ),
        ],
    )
