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
        upload_trigger=Output("table-upload-trigger", "data"),
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
    print(train_type)
    print(start_speed)
    print(end_speed)
    print(start_distance)
    print(end_distance)
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
    Input("table-upload-trigger", "data"),
)
def load_data_to_table_callback(_: int) -> list[TrainTypeTable]:
    """Колбэк для загрузки данных в таблицу"""
    db_data = TrainTypeDAO().get_all()
    mapped_data = TrainTypeMapper().model_to_table(db_data)
    return mapped_data
