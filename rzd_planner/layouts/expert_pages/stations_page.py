import dash_bootstrap_components as dbc
from dash_extensions.enrich import dcc, html

from rzd_planner.layouts.components.header import render_expert_header
from rzd_planner.layouts.components.table_component import render_table
from rzd_planner.layouts.components.table_header import render_table_header


def _render_modal() -> dbc.Modal:
    """Модальное окно для сохранения станций"""
    return dbc.Modal(
        children=[
            dbc.ModalHeader(dbc.ModalTitle("Добавление станции")),
            dbc.ModalBody(
                children=[
                    html.Div(
                        children=[
                            html.P("Название станции"),
                            dbc.Input(
                                id="stations-name-id",
                            ),
                        ],
                        className="stations-name-block",
                    ),
                    html.Div(
                        children=[
                            dbc.Button(
                                children="Сохранить",
                                id="stations-save-btn-id",
                            ),
                        ],
                        className="stations-save-btn-block",
                    ),
                ],
                className="stations-modal-body",
            ),
        ],
        id="stations-modal-id",
        is_open=False,
        centered=True,
    )


def render_stations_page() -> html.Div:
    """Функция для отрисовки страницы станций"""
    _cols_defs = [
        {"name": "Станция", "id": "station"},
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
                                disabled=True,
                            ),
                        ],
                    ),
                    render_table(table_id="stations-table-id", columns_def=_cols_defs),
                ],
                className="table-block",
            ),
            dcc.Store(id="stations-table-upload-trigger", storage_type="memory"),
        ],
    )
