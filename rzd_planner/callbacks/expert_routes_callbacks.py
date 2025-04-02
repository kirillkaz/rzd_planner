from typing import TypedDict

from dash_extensions.enrich import Input, Output, State, no_update
from sqlalchemy.exc import SQLAlchemyError

from rzd_planner.app import app
from rzd_planner.services.dao import (
    ExpertRouteDTO,
    ExpertRoutesDAO,
    StationsDAO,
)
from rzd_planner.services.mappers import (
    StationsMapper,
    StationsOption,
    TrainRoutesMapper,
    TrainRoutesTableType,
)


class SaveExpertRouteReturn(TypedDict):
    """Структура возвращаемого типа для колбэка save_train_type_callback"""

    modal_is_open: bool
    upload_trigger: str


@app.callback(
    Output("expert-routes-start-station-id", "options"),
    Output("expert-routes-end-station-id", "options"),
    Input("routes-expert-add-btn-id", "n_clicks"),
    prevent_initial_call=True,
)
def upload_exp_routes_stations(_: int) -> tuple[StationsOption, StationsOption]:
    """Колбэк для предзагрузки селекторов с станциями

    Returns:
        tuple[StationsOption, StationsOption]: Станции отправления и прибытия
    """
    objs = StationsDAO().get_all()
    return StationsMapper().model_to_options(
        objects=objs
    ), StationsMapper().model_to_options(objects=objs)


@app.callback(
    Output("expert-routes-modal-id", "is_open"),
    Input("routes-expert-add-btn-id", "n_clicks"),
    prevent_initial_call=True,
)
def open_exp_routes_modal_callback(_: int) -> bool:
    """Колбэк для открытия модального окна"""
    return True


@app.callback(
    output=dict(
        modal_is_open=Output("expert-routes-modal-id", "is_open"),
        upload_trigger=Output("exp-routes-table-upload-trigger", "data"),
    ),
    inputs=dict(
        _=Input("expert-routes-save-btn-id", "n_clicks"),
        start_station_id=State("expert-routes-start-station-id", "value"),
        end_station_id=State("expert-routes-end-station-id", "value"),
        distance=State("expert-routes-distance-id", "value"),
    ),
    prevent_initial_call=True,
)
def save_exp_route_callback(
    _: int,
    start_station_id: str,
    end_station_id: str,
    distance: str,
) -> SaveExpertRouteReturn:
    """Колбэк для сохранения маршрута

    Args:
        start_station_id (str): uuid станции отправления
        end_station_id (str): uuid станции прибытия
        distance (str): дальность маршрута

    Returns:
        SaveExpertRouteReturn: Структура возвращаемого типа для колбэка
    """
    print(start_station_id)
    print(end_station_id)
    print(distance)
    dto = ExpertRouteDTO(
        start_station_id=start_station_id,
        end_station_id=end_station_id,
        distance=distance,
    )

    try:
        ExpertRoutesDAO().save(dto=dto)
    except SQLAlchemyError as ex:
        print(ex)
        return SaveExpertRouteReturn(modal_is_open=True, upload_trigger=no_update)

    return SaveExpertRouteReturn(
        modal_is_open=False,
        upload_trigger="trigger",
    )


@app.callback(
    Output("routes-expert-table-id", "data"),
    Input("exp-routes-table-upload-trigger", "data"),
)
def load_exp_route_to_table(_: int) -> list[TrainRoutesTableType]:
    """Колбэк для загрузки данных в таблицу"""
    db_data = ExpertRoutesDAO().get_all()
    mapped_data = TrainRoutesMapper().model_to_table(db_data)
    return mapped_data
