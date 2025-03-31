import dash_bootstrap_components as dbc
from dash_extensions.enrich import html

from rzd_planner.layouts.components.header import render_expert_header
from rzd_planner.layouts.components.table_component import render_table
from rzd_planner.layouts.components.table_header import render_table_header


def render_stations_page() -> html.Div:
    """Функция для отрисовки страницы станций"""
    _cols_defs = [
        {"name": "Станция", "id": "station"},
    ]

    return html.Div(
        children=[
            render_expert_header(),
            html.Div(
                children=[
                    render_table_header(
                        left_childrens=[
                            html.Div(
                                "Таблица станций",
                                className="table-header-title",
                            )
                        ],
                        right_childrens=[
                            dbc.Button(
                                children="Добавить станцию",
                                color="secondary",
                                id="stations-add-btn-id",
                            ),
                            dbc.Button(
                                children="Удалить станции",
                                color="secondary",
                                id="stations-delete-btn-id",
                            ),
                        ],
                    ),
                    render_table(table_id="stations-table-id", columns_def=_cols_defs),
                ],
                className="table-block",
            ),
        ],
    )
