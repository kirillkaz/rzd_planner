from typing import TypedDict

from dash_extensions.enrich import Input, Output, State, no_update
from sqlalchemy.exc import SQLAlchemyError

from rzd_planner.app import app
from rzd_planner.services.dao import ExpertRoutesDAO, FullRoutesDAO, FullRoutesDTO
from rzd_planner.services.mappers import (
    FullRouteOption,
    FullRoutesMapper,
    FullRoutesTableType,
)
from rzd_planner.services.train_routes_service import TrainRoutesService


class SaveUserRouteReturn(TypedDict):
    """Структура возвращаемого типа для колбэка save_usr_route_callback"""

    modal_is_open: bool
    upload_trigger: str


class DelUserRoutesReturn(TypedDict):
    """Структура возвращаемого типа для колбэка del_usr_routes_callback"""

    trigger: str
    selected_rows: list[int]
    is_open: bool


@app.callback(
    Output("user-routes-select-id", "options"),
    Input("routes-user-add-btn-id", "n_clicks"),
    prevent_initial_call=True,
)
def upload_usr_routes_stations(_: int) -> list[FullRouteOption]:
    """Колбэк для предзагрузки селекторов с полными маршрутами

    Returns:
        list[FullRouteOption]: Полные маршруты
    """
    objs = ExpertRoutesDAO().get_all()
    raw_options = TrainRoutesService().get_train_routes(objs)
    print(raw_options)
    options = FullRoutesMapper().str_to_options(raw_options)
    print(options)
    return options


@app.callback(
    Output("user-routes-modal-id", "is_open"),
    Input("routes-user-add-btn-id", "n_clicks"),
    prevent_initial_call=True,
)
def open_usr_routes_modal_callback(_: int) -> bool:
    """Колбэк для открытия модального окна"""
    return True


@app.callback(
    output=dict(
        modal_is_open=Output("user-routes-modal-id", "is_open"),
        upload_trigger=Output("routes-user-table-upload-trigger", "data"),
    ),
    inputs=dict(
        _=Input("user-routes-save-btn-id", "n_clicks"),
        route=State("user-routes-select-id", "value"),
    ),
    prevent_initial_call=True,
)
def save_usr_route_callback(
    _: int,
    route: str,
) -> SaveUserRouteReturn:
    """Колбэк для сохранения полного маршрута

    Args:
        route (str): полный маршрут поездки

    Returns:
        SaveUserRouteReturn: Структура возвращаемого типа для колбэка
    """
    dto = FullRoutesDTO(
        route=route,
    )

    try:
        FullRoutesDAO().save(dto=dto)
    except SQLAlchemyError as ex:
        print(ex)
        return SaveUserRouteReturn(modal_is_open=True, upload_trigger=no_update)

    return SaveUserRouteReturn(
        modal_is_open=False,
        upload_trigger="trigger",
    )


@app.callback(
    Output("routes-user-table-id", "data"),
    Input("routes-user-table-upload-trigger", "data"),
)
def load_usr_route_to_table(_: int) -> list[FullRoutesTableType]:
    """Колбэк для загрузки данных в таблицу"""
    db_data = FullRoutesDAO().get_all()
    mapped_data = FullRoutesMapper().model_to_table(db_data)
    return mapped_data


@app.callback(
    Output("user-routes-delete-modal-id", "is_open"),
    Input("routes-user-delete-btn-id", "n_clicks"),
    prevent_initial_call=True,
)
def open_usr_routes_del_modal(_: int) -> bool:
    """Колбэк для открытия модального окна удаления маршрутов"""
    return True


@app.callback(
    output=dict(
        trigger=Output("routes-user-table-upload-trigger", "data"),
        selected_rows=Output("routes-user-table-id", "selected_rows"),
        is_open=Output("user-routes-delete-modal-id", "is_open"),
    ),
    inputs=dict(
        _=Input("user-routes-delete-confirm-btn-id", "n_clicks"),
        table_data=State("routes-user-table-id", "derived_virtual_data"),
        selected_indices=State("routes-user-table-id", "derived_virtual_selected_rows"),
    ),
    prevent_initial_call=True,
)
def del_usr_routes_callback(
    _: int,
    table_data: list[FullRoutesTableType],
    selected_indices: list[int],
) -> DelUserRoutesReturn:
    """Колбэк для удаления полных маршрутов

    Args:
        table_data (list[FullRoutesTableType]): данные таблицы
        selected_indices (list[int]): индексы выделенных строк

    Returns:
        DelUserRoutesReturn: возвращаемая структура колбэка
    """
    bad_uuids = []
    for index, elem in enumerate(table_data):
        if index in selected_indices:
            bad_uuids.append(elem["id"])

    FullRoutesDAO().delete(bad_uuids)
    return DelUserRoutesReturn(
        trigger="trigger",
        selected_rows=[],
        is_open=False,
    )
