from __future__ import annotations

from urllib.parse import urlparse

from dash.exceptions import PreventUpdate
from dash_extensions.enrich import Input, Output, ctx, html, no_update
from flask_login import current_user

from rzd_planner.app import app
from rzd_planner.config import UserRoles
from rzd_planner.layouts.auth_page import render_auth_page
from rzd_planner.layouts.expert_pages import (
    render_check_knowledge_page,
    render_routes_page,
    render_stations_page,
    render_train_types_page,
)
from rzd_planner.layouts.user_pages import (
    render_trains_page,
    render_travel_times_page,
    render_user_routes_page,
)
from rzd_planner.services.dao.users_dao import UserDAO


@app.callback(
    Output("page-content", "children"),
    Output("redirect", "pathname"),
    [Input("url", "pathname")],
)
def display_page(pathname: str) -> tuple[html.Div, str]:
    """Колбэк для отрисовки соответствующих страниц

    Args:
        pathname (str): путь к странице

    Returns:
        tuple[html.Div, str]: содержимое страницы + путь к странице
    """
    print(ctx.triggered)
    expert_pages = {
        "/train_type": render_train_types_page,
        "/stations": render_stations_page,
        "/routes_expert": render_routes_page,
        "/check_knowledge": render_check_knowledge_page,
    }

    user_pages = {
        "/trains": render_trains_page,
        "/travel_times": render_travel_times_page,
        "/routes_user": render_user_routes_page,
    }

    if pathname is None:
        raise PreventUpdate

    view = no_update
    url = no_update
    endpoint = urlparse(pathname)
    if pathname.endswith("/auth") or pathname == "/":
        view = render_auth_page()

    elif current_user.get_id() is None and endpoint in expert_pages.keys():
        view = render_auth_page()
        url = ""

    elif current_user.get_id():
        with app.server.app_context():
            user_role = UserDAO().get_role_by_username(current_user.get_id())
        if endpoint.path in expert_pages.keys() and user_role == str(UserRoles.EXPERT):
            view = expert_pages[endpoint.path]()

        elif endpoint.path in expert_pages.keys() and user_role == str(UserRoles.USER):
            view = user_pages[endpoint.path]()
        else:
            view = "404"

    else:
        view = "404"

    return view, url
