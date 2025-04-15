from typing import TypedDict

from dash_extensions.enrich import Input, Output, State, no_update
from sqlalchemy.exc import SQLAlchemyError

from rzd_planner.app import app
from rzd_planner.services.dao import TrainDAO, TrainDTO, TrainTypeDAO
from rzd_planner.services.mappers import (
    TrainsMapper,
    TrainsTableType,
    TrainTypeMapper,
    TrainTypeOption,
)
from rzd_planner.services.train_routes_service import TrainRoutesService


class SaveTrainReturn(TypedDict):
    """Структура возвращаемого типа для колбэка save_train_callback"""

    modal_is_open: bool
    upload_trigger: str


class DelTrainReturn(TypedDict):
    """Структура возвращаемого типа для колбэка del_trains_callback"""

    trigger: str
    selected_rows: list[int]
    is_open: bool

@app.callback(
    Output("train-type-select-id", "options"),
    Input("trains-add-btn-id", "n_clicks"),
    prevent_initial_call=True,
)
def upload_train_types(_: int) -> TrainTypeOption:
    """Колбэк для предзагрузки селекторов с типами поездов

    Returns:
        TrainTypeOption: типы поездов
    """
    objs = TrainTypeDAO().get_all()
    return TrainTypeMapper().model_to_options(objects=objs)


@app.callback(
    Output("train-modal-id", "is_open"),
    Input("trains-add-btn-id", "n_clicks"),
    prevent_initial_call=True,
)
def open_train_modal_callback(_: int) -> bool:
    """Колбэк для открытия модального окна"""
    return True


@app.callback(
    output=dict(
        modal_is_open=Output("train-modal-id", "is_open"),
        upload_trigger=Output("trains-table-upload-trigger", "data"),
    ),
    inputs=dict(
        _=Input("train-save-btn-id", "n_clicks"),
        train_number=State("train-input-id", "value"),
        train_type_uuid=State("train-type-select-id", "value"),
    ),
    prevent_initial_call=True,
)
def save_train_callback(
    _: int,
    train_number: str,
    train_type_uuid: str,
) -> SaveTrainReturn:
    """Колбэк для сохранения поезда

    Args:
        train_number (str): Номер поезда
        train_type_uuid (str): uuid типа поезда

    Returns:
        SaveTrainReturn: Структура возвращаемого типа для колбэка
    """
    dto = TrainDTO(
        train_number=train_number,
        train_type_id=train_type_uuid,
    )

    try:
        TrainDAO().save(dto=dto)
    except SQLAlchemyError as ex:
        print(ex)
        return SaveTrainReturn(modal_is_open=True, upload_trigger=no_update)

    return SaveTrainReturn(
        modal_is_open=False,
        upload_trigger="trigger",
    )


@app.callback(
    Output("trains-table-id", "data"),
    Input("trains-table-upload-trigger", "data"),
)
def load_exp_route_to_table(_: int) -> list[TrainsTableType]:
    """Колбэк для загрузки данных в таблицу"""

    db_data = TrainDAO().get_all()
    mapped_data = TrainsMapper().model_to_table(db_data)
    return mapped_data

@app.callback(
    Output("trains-delete-modal-id", "is_open"),
    Input("trains-delete-btn-id", "n_clicks"),
    prevent_initial_call=True,
)
def open_trains_del_modal(_: int) -> bool:
    """Колбэк для открытия модального окна удаления поездов"""
    return True


@app.callback(
    output=dict(
        trigger=Output("trains-table-upload-trigger", "data"),
        selected_rows=Output("trains-table-id", "selected_rows"),
        is_open=Output("trains-delete-modal-id", "is_open"),
    ),
    inputs=dict(
        _=Input("trains-delete-confirm-btn-id", "n_clicks"),
        table_data=State("trains-table-id", "derived_virtual_data"),
        selected_indices=State("trains-table-id", "derived_virtual_selected_rows"),
    ),
    prevent_initial_call=True,
)
def del_trains_callback(
    _: int,
    table_data: list[TrainsTableType],
    selected_indices: list[int],
) -> DelTrainReturn:
    """Колбэк для удаления поездов

    Args:
        table_data (list[TrainsTableType]): данные таблицы
        selected_indices (list[int]): индексы выделенных строк

    Returns:
        DelTrainReturn: возвращаемая структура колбэка
    """
    bad_uuids = []
    for index, elem in enumerate(table_data):
        if index in selected_indices:
            bad_uuids.append(elem["id"])

    TrainDAO().delete(bad_uuids)
    return DelTrainReturn(
        trigger="trigger",
        selected_rows=[],
        is_open=False,
    )