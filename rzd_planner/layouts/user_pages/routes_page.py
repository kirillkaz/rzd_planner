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
            dbc.ModalHeader(dbc.ModalTitle("Добавление маршрута")),
            dbc.ModalBody(
                children=[
                    html.Div(
                        children=[
                            html.Div(
                                children=[
                                    html.Div(
                                        children=[
                                            html.P("Маршрут:"),
                                            dbc.Select(id="user-routes-select-id"),
                                            dbc.FormFeedback(
                                                "Это поле обязательно для заполнения!",
                                                type="invalid",
                                            ),
                                        ]
                                    ),
                                    html.Div(
                                        children=[
                                            html.P("Номер подходящего поезда:"),
                                            dbc.Select(
                                                id="user-routes-select-train-id"
                                            ),
                                            dbc.FormFeedback(
                                                "Это поле обязательно для заполнения!",
                                                type="invalid",
                                            ),
                                        ]
                                    ),
                                    html.Div(
                                        children=[
                                            html.P("Дальность поездки:"),
                                            dbc.Input(
                                                id="user-routes-distance-id",
                                                readonly=True,
                                                type="number",
                                            ),
                                            dbc.FormFeedback(
                                                "Нет походящих поездов на данную дистанцию!",
                                                type="invalid",
                                            ),
                                        ]
                                    ),
                                ],
                                className="modal-user-routes-block",
                            ),
                        ],
                        className="user-routes-modal-body-inner",
                    ),
                    html.Div(
                        children=[
                            dbc.Button(
                                children="Сохранить",
                                id="user-routes-save-btn-id",
                            ),
                        ],
                        className="user-routes-save-btn-block",
                    ),
                ],
                className="user-routes-modal-body",
            ),
        ],
        id="user-routes-modal-id",
        is_open=False,
        centered=True,
    )


def render_user_routes_page() -> html.Div:
    """Функция для отрисовки страницы маршрутов станций"""
    _cols_defs = [
        {"name": "Номер поезда", "id": "train"},
        {"name": "Маршрут поездки", "id": "route"},
        {"name": "Дальность поездки", "id": "distance"},
    ]

    return html.Div(
        children=[
            render_delete_modal(
                title="Удаление маршрута",
                button_id="user-routes-delete-confirm-btn-id",
                modal_id="user-routes-delete-modal-id",
            ),
            _render_modal(),
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
            dcc.Store(
                "routes-user-table-upload-trigger", storage_type="memory", data={}
            ),
        ],
    )
