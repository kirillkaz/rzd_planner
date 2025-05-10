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
                                    html.P("Маршрут поездки:"),
                                    dbc.Select(id="travel-time-route-input-id"),
                                    dbc.FormFeedback(
                                        "Это поле обязательно для заполнения!",
                                        type="invalid",
                                    ),
                                ],
                                className="modal-travel-time-block",
                            ),
                            html.Div(
                                children=[
                                    html.P("Время поездки:"),
                                    html.Div(
                                        children=[
                                            html.Div(
                                                children=[
                                                    html.P("Дни:"),
                                                    dbc.Input(
                                                        type="number",
                                                        id="travel-time-days-id",
                                                    ),
                                                    dbc.FormFeedback(
                                                        "Это поле обязательно для заполнения. Значение должно быть больше нуля.",
                                                        type="invalid",
                                                    ),
                                                ]
                                            ),
                                            html.Div(
                                                children=[
                                                    html.P("Часы:"),
                                                    dbc.Input(
                                                        type="number",
                                                        id="travel-time-hours-id",
                                                    ),
                                                    dbc.FormFeedback(
                                                        "Это поле обязательно для заполнения. Значение должно быть больше нуля.",
                                                        type="invalid",
                                                    ),
                                                ]
                                            ),
                                            html.Div(
                                                children=[
                                                    html.P("Минуты:"),
                                                    dbc.Input(
                                                        type="number",
                                                        id="travel-time-minutes-id",
                                                    ),
                                                    dbc.FormFeedback(
                                                        "Это поле обязательно для заполнения. Значение должно быть больше нуля.",
                                                        type="invalid",
                                                    ),
                                                ]
                                            ),
                                        ],
                                        className="modal-travel-total-time-block",
                                    ),
                                ],
                                className="modal-travel-time-input-block",
                            ),
                        ],
                        className="travel-time-modal-body-inner",
                    ),
                    html.Div(
                        children=[
                            dbc.Button(
                                children="Сохранить",
                                id="travel-time-save-btn-id",
                            ),
                        ],
                        className="travel-time-save-btn-block",
                    ),
                ],
                className="travel-time-modal-body",
            ),
        ],
        id="travel-time-modal-id",
        is_open=False,
        centered=True,
    )


def render_travel_times_page() -> html.Div:
    """Функция для отрисовки страницы времени поездки"""
    _cols_defs = [
        {"name": "Маршрут поездки", "id": "train_route"},
        {"name": "Время поездки", "id": "total_time"},
    ]

    return html.Div(
        children=[
            render_delete_modal(
                "Удаление времени поездки",
                "travel-time-delete-confirm-btn-id",
                "travel-time-delete-modal-id",
            ),
            _render_modal(),
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
            dcc.Store(id="travel-times-table-upload-trigger", storage_type="memory"),
        ],
    )
