import dash_bootstrap_components as dbc
from dash_extensions.enrich import html, dcc

from rzd_planner.layouts.components.header import render_expert_header
from rzd_planner.layouts.components.table_component import render_table
from rzd_planner.layouts.components.table_header import render_table_header


def _render_modal() -> dbc.Modal:
    """Функция для отрисовки модального окна"""
    return dbc.Modal(
        children=[
            dbc.ModalHeader(dbc.ModalTitle("Добавление типа поезда")),
            dbc.ModalBody(
                children=[
                    html.Div(
                        children=[
                            html.Div(
                                children=[
                                    html.P("Тип поезда:"),
                                    dbc.Input(id="train-type-input-id"),
                                ],
                                className="modal-train-type-block",
                            ),
                            html.Div(
                                children=[
                                    html.P("Скорость поезда в км/ч:"),
                                    html.Div(
                                        children=[
                                            html.Div(
                                                children=[
                                                    html.P("От"),
                                                    dbc.Input(
                                                        id="train-type-start-speed-id",
                                                        type="number",
                                                    ),
                                                ],
                                            ),
                                            html.Div(
                                                children=[
                                                    html.P("До"),
                                                    dbc.Input(
                                                        id="train-type-end-speed-id",
                                                        type="number",
                                                    ),
                                                ],
                                            ),
                                        ],
                                        className="modal-train-type-speed-block",
                                    ),
                                ],
                            ),
                            html.Div(
                                children=[
                                    html.P("Дальность поезда в км:"),
                                    html.Div(
                                        children=[
                                            html.Div(
                                                children=[
                                                    html.P("От"),
                                                    dbc.Input(
                                                        id="train-type-start-distance-id",
                                                        type="number",
                                                    ),
                                                ],
                                            ),
                                            html.Div(
                                                children=[
                                                    html.P("До"),
                                                    dbc.Input(
                                                        id="train-type-end-distance-id",
                                                        type="number",
                                                    ),
                                                ],
                                            ),
                                        ],
                                        className="modal-train-type-distance-block",
                                    ),
                                ],
                            ),
                        ],
                        className="train-type-modal-body-inner",
                    ),
                    html.Div(
                        children=[
                            dbc.Button(
                                children="Сохранить",
                                id="train-type-save-btn-id",
                            ),
                        ],
                        className="train-type-save-btn-block",
                    ),
                ],
                className="train-type-modal-body",
            ),
        ],
        id="train-type-modal-id",
        is_open=False,
        centered=True,
    )


def render_train_types_page() -> html.Div:
    """Функция для отрисовки типов поездов"""

    _cols_defs = [
        {"name": "Тип поезда", "id": "train_type"},
        {"name": "Скорость", "id": "speed"},
        {"name": "Дальность поездки", "id": "travel_distance"},
    ]

    return html.Div(
        children=[
            _render_modal(),
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
            dcc.Store(id="table-upload-trigger", storage_type="memory")
        ],
    )
