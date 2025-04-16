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


class DelTravelTimesReturn(TypedDict):
    """Структура возвращаемого типа для колбэка del_travel_times_callback"""

    trigger: str
    selected_rows: list[int]
    is_open: bool


@app.callback(
    Output("travel-time-route-input-id", "options"),
    Input("travel-times-add-btn-id", "n_clicks"),
    prevent_initial_call=True,
)
def upload_travel_times_callback(_: int) -> list[FullRouteOption]:
    """Колбэк для предзагрузки селектора с маршрутами поездок

    Returns:
        list[FullRouteOption]: маршруты поездок
    """
    objs = FullRoutesDAO().get_all()
    return FullRoutesMapper().model_to_options(objects=objs)


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
    ),
    inputs=dict(
        _=Input("travel-time-save-btn-id", "n_clicks"),
        train_route_id=State("travel-time-route-input-id", "value"),
        start_date=State("travel-time-start-date-id", "value"),
        end_date=State("travel-time-end-date-id", "value"),
    ),
    prevent_initial_call=True,
)
def save_travel_times_callback(
    _: int,
    train_route_id: str,
    start_date: str,
    end_date: str,
) -> SaveTravelTimesReturn:
    """Колбэк для сохранения маршрута

    Args:
        train_route_id (str): uuid полного маршрута поездки
        start_date (str): время отправления поезда
        disend_datetance (str): время прибытия поезда

    Returns:
        SaveTravelTimesReturn: Структура возвращаемого типа для колбэка
    """
    dto = TrainTravelTimesDTO(
        train_route_id=train_route_id,
        start_date=start_date,
        end_date=end_date,
    )

    try:
        TrainTravelTimesDAO().save(dto=dto)
    except SQLAlchemyError as ex:
        print(ex)
        return SaveTravelTimesReturn(modal_is_open=True, upload_trigger=no_update)

    return SaveTravelTimesReturn(
        modal_is_open=False,
        upload_trigger="trigger",
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