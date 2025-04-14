from typing import TypedDict

from dash_extensions.enrich import Input, Output, State, no_update
from sqlalchemy.exc import SQLAlchemyError

from rzd_planner.app import app
from rzd_planner.services.dao import TrainTypeDAO, TrainTypeDTO
from rzd_planner.services.mappers import TrainTypeMapper, TrainTypeTable


class SaveTrainTypeReturn(TypedDict):
    """Структура возвращаемого типа для колбэка save_train_type_callback"""

    modal_is_open: bool
    upload_trigger: str


class DelTrainTypeReturn(TypedDict):
    """Структура возвращаемого типа для колбэка del_train_types_callback"""

    trigger: str
    selected_rows: list[int]
    is_open: bool


@app.callback(
    Output("train-type-modal-id", "is_open"),
    Input("train-types-add-btn-id", "n_clicks"),
    prevent_initial_call=True,
)
def open_modal_callback(_: int) -> bool:
    """Колбэк для открытия модального окна"""
    return True


@app.callback(
    output=dict(
        modal_is_open=Output("train-type-modal-id", "is_open"),
        upload_trigger=Output("table-type-table-upload-trigger", "data"),
    ),
    inputs=dict(
        _=Input("train-type-save-btn-id", "n_clicks"),
        train_type=State("train-type-input-id", "value"),
        start_speed=State("train-type-start-speed-id", "value"),
        end_speed=State("train-type-end-speed-id", "value"),
        start_distance=State("train-type-start-distance-id", "value"),
        end_distance=State("train-type-end-distance-id", "value"),
    ),
    prevent_initial_call=True,
)
def save_train_type_callback(
    _: int,
    train_type: str,
    start_speed: float,
    end_speed: float,
    start_distance: float,
    end_distance: float,
) -> SaveTrainTypeReturn:
    dto = TrainTypeDTO(
        name=train_type,
        min_speed=start_speed,
        max_speed=end_speed,
        min_distance=start_distance,
        max_distance=end_distance,
    )

    try:
        TrainTypeDAO().save(dto=dto)
    except SQLAlchemyError as ex:
        print(ex)
        return SaveTrainTypeReturn(modal_is_open=True, upload_trigger=no_update)

    return SaveTrainTypeReturn(
        modal_is_open=False,
        upload_trigger="trigger",
    )


@app.callback(
    Output("train-types-table-id", "data"),
    Input("table-type-table-upload-trigger", "data"),
)
def load_data_to_table_callback(_: int) -> list[TrainTypeTable]:
    """Колбэк для загрузки данных в таблицу"""
    db_data = TrainTypeDAO().get_all()
    mapped_data = TrainTypeMapper().model_to_table(db_data)
    return mapped_data


@app.callback(
    Output("train-types-delete-modal-id", "is_open"),
    Input("train-types-delete-btn-id", "n_clicks"),
    prevent_initial_call=True,
)
def open_train_types_del_modal(_: int) -> bool:
    """Колбэк для открытия модального окна удаления типов поездов"""
    return True


@app.callback(
    output=dict(
        trigger=Output("table-type-table-upload-trigger", "data"),
        selected_rows=Output("train-types-table-id", "selected_rows"),
        is_open=Output("train-types-delete-modal-id", "is_open"),
    ),
    inputs=dict(
        _=Input("train-types-delete-confirm-btn-id", "n_clicks"),
        table_data=State("train-types-table-id", "derived_virtual_data"),
        selected_indices=State("train-types-table-id", "derived_virtual_selected_rows"),
    ),
    prevent_initial_call=True,
)
def del_train_types_callback(
    _: int,
    table_data: list[TrainTypeTable],
    selected_indices: list[int],
) -> DelTrainTypeReturn:
    """Колбэк для удаления типов поездов

    Args:
        table_data (list[TrainTypeTable]): данные таблицы
        selected_indices (list[int]): индексы выделенных строк

    Returns:
        DelTrainTypeReturn: возвращаемая структура колбэка
    """
    bad_uuids = []
    for index, elem in enumerate(table_data):
        if index in selected_indices:
            bad_uuids.append(elem["id"])

    TrainTypeDAO().delete(bad_uuids)
    return DelTrainTypeReturn(
        trigger="trigger",
        selected_rows=[],
        is_open=False,
    )
