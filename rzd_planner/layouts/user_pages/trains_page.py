import dash_bootstrap_components as dbc
from dash_extensions.enrich import dcc, html

from rzd_planner.layouts.components.del_modal_component import render_delete_modal
from rzd_planner.layouts.components.header import render_user_header
from rzd_planner.layouts.components.table_component import render_table
from rzd_planner.layouts.components.table_header import render_table_header


def _render_modal() -> dbc.Modal:
    """Функция для отрисовки модального окна"""
    return dbc.Modal(
        children=[
            dbc.ModalHeader(dbc.ModalTitle("Добавление поезда")),
            dbc.ModalBody(
                children=[
                    html.Div(
                        children=[
                            html.Div(
                                children=[
                                    html.P("Номер поезда:"),
                                    dbc.Input(id="train-input-id"),
                                ],
                                className="modal-train-block",
                            ),
                            html.Div(
                                children=[
                                    html.P("Тип поезда:"),
                                    dbc.Select(id="train-type-select-id"),
                                ],
                                className="modal-train-type-select-block",
                            ),
                        ],
                        className="train-modal-body-inner",
                    ),
                    html.Div(
                        children=[
                            dbc.Button(
                                children="Сохранить",
                                id="train-save-btn-id",
                            ),
                        ],
                        className="train-save-btn-block",
                    ),
                ],
                className="train-modal-body",
            ),
        ],
        id="train-modal-id",
        is_open=False,
        centered=True,
    )


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
            render_delete_modal(
                "Удаление поездов",
                "trains-delete-confirm-btn-id",
                "trains-delete-modal-id",
            ),
            _render_modal(),
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
            dcc.Store("trains-table-upload-trigger", storage_type="memory", data={}),
        ],
    )
