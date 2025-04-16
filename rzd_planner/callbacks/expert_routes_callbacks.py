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


class DelExpertRoutesReturn(TypedDict):
    """Структура возвращаемого типа для колбэка del_expert_routes_callback"""

    trigger: str
    selected_rows: list[int]
    is_open: bool


@app.callback(
    Output("expert-routes-start-station-id", "options"),
    Output("expert-routes-end-station-id", "options"),
    Input("routes-expert-add-btn-id", "n_clicks"),
    prevent_initial_call=True,
)
def upload_exp_routes_callback(_: int) -> tuple[StationsOption, StationsOption]:
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


@app.callback(
    Output("expert-routes-delete-modal-id", "is_open"),
    Input("routes-expert-delete-btn-id", "n_clicks"),
    prevent_initial_call=True,
)
def open_expert_routes_del_modal(_: int) -> bool:
    """Колбэк для открытия модального окна удаления маршрутов"""
    return True


@app.callback(
    output=dict(
        trigger=Output("exp-routes-table-upload-trigger", "data"),
        selected_rows=Output("routes-expert-table-id", "selected_rows"),
        is_open=Output("expert-routes-delete-modal-id", "is_open"),
    ),
    inputs=dict(
        _=Input("expert-routes-delete-confirm-btn-id", "n_clicks"),
        table_data=State("routes-expert-table-id", "derived_virtual_data"),
        selected_indices=State(
            "routes-expert-table-id", "derived_virtual_selected_rows"
        ),
    ),
    prevent_initial_call=True,
)
def del_expert_routes_callback(
    _: int,
    table_data: list[TrainRoutesTableType],
    selected_indices: list[int],
) -> DelExpertRoutesReturn:
    """Колбэк для удаления маршрутов

    Args:
        table_data (list[TrainRoutesTableType]): данные таблицы
        selected_indices (list[int]): индексы выделенных строк

    Returns:
        DelExpertRoutesReturn: возвращаемая структура колбэка
    """
    bad_uuids = []
    for index, elem in enumerate(table_data):
        if index in selected_indices:
            bad_uuids.append(elem["id"])

    ExpertRoutesDAO().delete(bad_uuids)
    return DelExpertRoutesReturn(
        trigger="trigger",
        selected_rows=[],
        is_open=False,
    )
