from datetime import datetime, timedelta

import dash_bootstrap_components as dbc
from dash_extensions.enrich import dcc, html

from rzd_planner.layouts.components.header import render_user_header


def render_planning_page() -> html.Div:
    """Функция для отрисовки страницы формирования расписания"""

    return html.Div(
        children=[
            render_user_header(),
            html.Div(
                children=[
                    dcc.DatePickerRange(
                        id="planning-date-picker-id",
                        start_date=datetime.now().date(),
                        end_date=datetime.now().date() + timedelta(days=2),
                    ),
                    dbc.Button(
                        children="Сформировать расписание", id="scheduling-button-id"
                    ),
                    dcc.Download(id="scheduling-download-id"),
                ],
                className="planning-page-tools-block",
            ),
        ],
    )
