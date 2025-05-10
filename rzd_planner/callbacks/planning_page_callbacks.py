from typing import Any

from dash_extensions.enrich import Input, Output, State, dcc
from dateutil.parser import parse

from rzd_planner.app import app
from rzd_planner.services.schedule_planning_service import SchedulePlanner


@app.callback(
    Output("scheduling-download-id", "data"),
    Input("scheduling-button-id", "n_clicks"),
    State("planning-date-picker-id", "start_date"),
    State("planning-date-picker-id", "end_date"),
    prevent_initial_call=True,
)
def get_shedule_plan_callback(
    _: int, start_date: str, end_date: str
) -> dict[str, Any | None]:
    """Колбэк для составления расписания ЖД перевозок

    Args:
        start_date (str): Дата начала составления расписания
        end_date (str): Дата конца составления расписания

    Returns:
        dict[str, Any | None]: Расписание жд перевозок
    """
    start_date_dt = parse(start_date)
    end_date_dt = parse(end_date)

    planner_data = SchedulePlanner().execute(
        start_date=start_date_dt, end_date=end_date_dt
    )

    return dcc.send_data_frame(
        planner_data.to_excel, "Расписание ЖД перевозок.xlsx", index=False
    )
