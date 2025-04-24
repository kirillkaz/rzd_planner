from typing import TypedDict

from dash_extensions.enrich import Input, Output, State, no_update
from sqlalchemy.exc import SQLAlchemyError

from rzd_planner.app import app
from rzd_planner.services.dao import (
    ExpertRoutesDAO,
    FullRoutesDAO,
    FullRoutesDTO,
    TrainDAO,
)
from rzd_planner.services.mappers import (
    FullRouteOption,
    FullRoutesMapper,
    FullRoutesTableType,
    TrainsMapper,
)
from rzd_planner.services.routes_distance_calc_service import RoutesDistanceCalc
from rzd_planner.services.train_routes_service import TrainRoutesService


class SaveUserRouteReturn(TypedDict):
    """Структура возвращаемого типа для колбэка save_usr_route_callback"""

    modal_is_open: bool
    upload_trigger: str
    route_is_invalid: bool


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
    options = FullRoutesMapper().str_to_options(raw_options)
    return options


@app.callback(
    Output("user-routes-select-train-id", "options"),
    Output("user-routes-distance-id", "invalid"),
    Input("user-routes-distance-id", "value"),
    prevent_initial_call=True,
)
def upload_usr_routes_trains(distance: int) -> tuple[list[FullRouteOption], bool]:
    """Колбэк для предзагрузки селекторов с поездами

    Returns:
        tuple[list[FullRouteOption], bool]: поезда + инвалидность поля
    """
    objs = TrainDAO().get_all_free_by_distance_not(distance)
    options = TrainsMapper().model_to_options(objs)
    trains_is_invalid = not bool(options)

    return options, trains_is_invalid


@app.callback(
    Output("user-routes-distance-id", "value"),
    Input("user-routes-select-id", "value"),
    prevent_initial_call=True,
)
def upload_distance_field(route: str) -> float:
    """Колбэк для обновления дистанции поездки для маршрута"""

    return RoutesDistanceCalc().calc_distance(route)


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
        route_is_invalid=Output("user-routes-select-id", "invalid"),
    ),
    inputs=dict(
        _=Input("user-routes-save-btn-id", "n_clicks"),
        route=State("user-routes-select-id", "value"),
        train_id=State("user-routes-select-train-id", "value"),
        distance=State("user-routes-distance-id", "value"),
    ),
    prevent_initial_call=True,
)
def save_usr_route_callback(
    _: int,
    route: str,
    train_id: str,
    distance: float,
) -> SaveUserRouteReturn:
    """Колбэк для сохранения полного маршрута

    Args:
        route (str): полный маршрут поездки
        train_id (str): uuid поезда
        distance (float): длина маршрута

    Returns:
        SaveUserRouteReturn: Структура возвращаемого типа для колбэка
    """
    dto = FullRoutesDTO(
        route=route,
        train_id=train_id,
        distance=distance,
    )

    route_invalid = not bool(route)
    if any([route_invalid]):
        return SaveUserRouteReturn(
            modal_is_open=True,
            upload_trigger=no_update,
            route_is_invalid=route_invalid,
        )

    try:
        FullRoutesDAO().save(dto=dto)
    except SQLAlchemyError as ex:
        print(ex)
        return SaveUserRouteReturn(
            modal_is_open=True,
            upload_trigger=no_update,
            route_is_invalid=route_invalid,
        )

    return SaveUserRouteReturn(
        modal_is_open=False,
        upload_trigger="trigger",
        route_is_invalid=route_invalid,
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
