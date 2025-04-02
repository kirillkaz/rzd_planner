from typing import TypedDict

from dash_extensions.enrich import Input, Output, State, no_update
from sqlalchemy.exc import SQLAlchemyError

from rzd_planner.app import app
from rzd_planner.services.dao import StationsDAO, StationsDTO
from rzd_planner.services.mappers import StationsMapper, StationsTableType


class SaveStationReturn(TypedDict):
    """Структура возвращаемого типа для колбэка save_train_type_callback"""

    modal_is_open: bool
    upload_trigger: str


@app.callback(
    Output("stations-modal-id", "is_open"),
    Input("stations-add-btn-id", "n_clicks"),
    prevent_initial_call=True,
)
def open_modal_stations_callback(_: int) -> bool:
    """Колбэк для открытия модального окна"""
    return True


@app.callback(
    output=dict(
        modal_is_open=Output("stations-modal-id", "is_open"),
        upload_trigger=Output("stations-table-upload-trigger", "data"),
    ),
    inputs=dict(
        _=Input("stations-save-btn-id", "n_clicks"),
        station_name=State("stations-name-id", "value"),
    ),
    prevent_initial_call=True,
)
def save_train_type_callback(
    _: int,
    station_name: str,
) -> SaveStationReturn:
    """Колбэк для сохранения станции

    Args:
        station_name (str): название станции

    Returns:
        SaveStationReturn: Структура возвращаемого типа для колбэка
    """
    print(station_name)
    dto = StationsDTO(
        name=station_name,
    )

    try:
        StationsDAO().save(dto=dto)
    except SQLAlchemyError as ex:
        print(ex)
        return SaveStationReturn(modal_is_open=True, upload_trigger=no_update)

    return SaveStationReturn(
        modal_is_open=False,
        upload_trigger="trigger",
    )


@app.callback(
    Output("stations-table-id", "data"),
    Input("stations-table-upload-trigger", "data"),
)
def load_data_to_table_callback(_: int) -> list[StationsTableType]:
    """Колбэк для загрузки данных в таблицу"""
    db_data = StationsDAO().get_all()
    mapped_data = StationsMapper().model_to_table(db_data)
    return mapped_data
