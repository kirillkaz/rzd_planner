from datetime import timedelta
from typing import TypedDict

from dash_extensions.enrich import Input, Output, State, no_update
from sqlalchemy.exc import SQLAlchemyError

from rzd_planner.app import app
from rzd_planner.services.dao import (
    FullRoutesDAO,
    TrainTravelTimesDAO,
    TrainTravelTimesDTO,
)
from rzd_planner.services.mappers import (
    FullRouteOption,
    FullRoutesMapper,
    TrainTravelTimesMapper,
    TrainTravelTimesTableType,
)


class SaveTravelTimesReturn(TypedDict):
    """Структура возвращаемого типа для колбэка save_travel_times_callback"""

    modal_is_open: bool
    upload_trigger: str
    train_route_id_is_invalid: bool
    days_is_valid: bool
    hours_is_valid: bool
    minutes_is_valid: bool


class DelTravelTimesReturn(TypedDict):
    """Структура возвращаемого типа для колбэка del_travel_times_callback"""

    trigger: str
    selected_rows: list[int]
    is_open: bool


@app.callback(
    Output("travel-time-route-input-id", "options"),
    Output("travel-time-route-input-id", "value"),
    Output("travel-time-route-input-id", "label"),
    Input("travel-times-add-btn-id", "n_clicks"),
    prevent_initial_call=True,
)
def upload_travel_times_callback(_: int) -> tuple[list[FullRouteOption], str, str]:
    """Колбэк для предзагрузки селектора с маршрутами поездок

    Returns:
        tuple[list[FullRouteOption], str, str]: маршруты поездок + значение и отображение 1й строки
    """
    objs = FullRoutesDAO().get_all_not_in_times()
    mapped_objs = FullRoutesMapper().model_to_options(objects=objs)

    if objs:
        return (
            mapped_objs,
            mapped_objs[0]["value"],
            mapped_objs[0]["label"],
        )
    return mapped_objs, no_update, no_update


@app.callback(
    Output("travel-time-modal-id", "is_open"),
    Input("travel-times-add-btn-id", "n_clicks"),
    prevent_initial_call=True,
)
def open_travel_times_modal_callback(_: int) -> bool:
    """Колбэк для открытия модального окна"""
    return True


@app.callback(
    output=dict(
        modal_is_open=Output("travel-time-modal-id", "is_open"),
        upload_trigger=Output("travel-times-table-upload-trigger", "data"),
        train_route_id_is_valid=Output("travel-time-route-input-id", "invalid"),
        days_is_valid=Output("travel-time-days-id", "invalid"),
        hours_is_valid=Output("travel-time-hours-id", "invalid"),
        minutes_is_valid=Output("travel-time-minutes-id", "invalid"),
    ),
    inputs=dict(
        _=Input("travel-time-save-btn-id", "n_clicks"),
        train_route_id=State("travel-time-route-input-id", "value"),
        days=State("travel-time-days-id", "value"),
        hours=State("travel-time-hours-id", "value"),
        minutes=State("travel-time-minutes-id", "value"),
    ),
    prevent_initial_call=True,
)
def save_travel_times_callback(
    _: int,
    train_route_id: str,
    days: int,
    hours: int,
    minutes: int,
) -> SaveTravelTimesReturn:
    """Колбэк для сохранения маршрута

    Args:
        train_route_id (str): uuid полного маршрута поездки
        days (int): Количество дней в пути
        hours (int): Количество часов в пути
        minutes (int): Количество минут в пути

    Returns:
        SaveTravelTimesReturn: Структура возвращаемого типа для колбэка
    """
    print(train_route_id)
    train_route_id_invalid = not bool(train_route_id)
    days_invalid = days is None or days < 0
    hours_invalid = hours is None or hours < 0
    minutes_invalid = minutes is None or minutes < 0

    if any([train_route_id_invalid, days_invalid, hours_invalid, minutes_invalid]):
        return SaveTravelTimesReturn(
            modal_is_open=True,
            upload_trigger=no_update,
            train_route_id_is_valid=train_route_id_invalid,
            days_is_valid=days_invalid,
            hours_is_valid=hours_invalid,
            minutes_is_valid=minutes_invalid,
        )

    total_time = timedelta(days=days, hours=hours, minutes=minutes).total_seconds()

    dto = TrainTravelTimesDTO(
        train_route_id=train_route_id,
        total_time=total_time,
    )

    try:
        TrainTravelTimesDAO().save(dto=dto)
    except SQLAlchemyError as ex:
        print(ex)
        return SaveTravelTimesReturn(
            modal_is_open=True,
            upload_trigger=no_update,
            train_route_id_is_valid=train_route_id_invalid,
            days_is_valid=days_invalid,
            hours_is_valid=hours_invalid,
            minutes_is_valid=minutes_invalid,
        )

    return SaveTravelTimesReturn(
        modal_is_open=False,
        upload_trigger="trigger",
        train_route_id_is_valid=train_route_id_invalid,
        days_is_valid=days_invalid,
        hours_is_valid=hours_invalid,
        minutes_is_valid=minutes_invalid,
    )


@app.callback(
    Output("travel-times-table-id", "data"),
    Input("travel-times-table-upload-trigger", "data"),
)
def load_travel_times_to_table(_: int) -> list[TrainTravelTimesTableType]:
    """Колбэк для загрузки данных в таблицу"""
    db_data = TrainTravelTimesDAO().get_all()
    mapped_data = TrainTravelTimesMapper().model_to_table(db_data)
    return mapped_data


@app.callback(
    Output("travel-time-delete-modal-id", "is_open"),
    Input("travel-times-delete-btn-id", "n_clicks"),
    prevent_initial_call=True,
)
def open_travel_times_del_modal(_: int) -> bool:
    """Колбэк для открытия модального окна удаление времени поездки"""
    return True


@app.callback(
    output=dict(
        trigger=Output("travel-times-table-upload-trigger", "data"),
        selected_rows=Output("travel-times-table-id", "selected_rows"),
        is_open=Output("travel-time-delete-modal-id", "is_open"),
    ),
    inputs=dict(
        _=Input("travel-time-delete-confirm-btn-id", "n_clicks"),
        table_data=State("travel-times-table-id", "derived_virtual_data"),
        selected_indices=State(
            "travel-times-table-id", "derived_virtual_selected_rows"
        ),
    ),
    prevent_initial_call=True,
)
def del_travel_times_callback(
    _: int,
    table_data: list[TrainTravelTimesTableType],
    selected_indices: list[int],
) -> DelTravelTimesReturn:
    """Колбэк для удаления времени поездки

    Args:
        table_data (list[TrainTravelTimesTableType]): данные таблицы
        selected_indices (list[int]): индексы выделенных строк

    Returns:
        DelTravelTimesReturn: возвращаемая структура колбэка
    """
    bad_uuids = []
    for index, elem in enumerate(table_data):
        if index in selected_indices:
            bad_uuids.append(elem["id"])

    TrainTravelTimesDAO().delete(bad_uuids)
    return DelTravelTimesReturn(
        trigger="trigger",
        selected_rows=[],
        is_open=False,
    )
