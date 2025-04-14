import dash_bootstrap_components as dbc
from dash_extensions.enrich import dcc, html

from rzd_planner.layouts.components.del_modal_component import render_delete_modal
from rzd_planner.layouts.components.header import render_expert_header
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
                                    html.P("Станция отправления:"),
                                    dbc.Select(id="expert-routes-start-station-id"),
                                ],
                                className="modal-expert-routes-block",
                            ),
                            html.Div(
                                children=[
                                    html.P("Станция прибытия:"),
                                    dbc.Select(id="expert-routes-end-station-id"),
                                ],
                                className="modal-expert-routes-block",
                            ),
                            html.Div(
                                children=[
                                    html.P("Дальность поездки в км:"),
                                    dbc.Input(
                                        id="expert-routes-distance-id",
                                        type="number",
                                    ),
                                ],
                                className="modal-expert-routes-block",
                            ),
                        ],
                        className="expert-routes-modal-body-inner",
                    ),
                    html.Div(
                        children=[
                            dbc.Button(
                                children="Сохранить",
                                id="expert-routes-save-btn-id",
                            ),
                        ],
                        className="expert-routes-save-btn-block",
                    ),
                ],
                className="expert-routes-modal-body",
            ),
        ],
        id="expert-routes-modal-id",
        is_open=False,
        centered=True,
    )


def render_routes_page() -> html.Div:
    """Функция для отрисовки страницы маршрутов"""
    _cols_defs = [
        {"name": "Станция отправления", "id": "start_station"},
        {"name": "Станция прибытия", "id": "end_station"},
        {"name": "Дальность маршрута, Км/ч", "id": "route_distance"},
    ]

    return html.Div(
        children=[
            render_delete_modal(
                "Удаление маршрутов",
                "expert-routes-delete-confirm-btn-id",
                "expert-routes-delete-modal-id",
            ),
            _render_modal(),
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
            dcc.Store(id="exp-routes-table-upload-trigger", storage_type="memory"),
        ],
    )
