from dash.development.base_component import Component
from dash_extensions.enrich import html


def render_table_header(
    left_childrens: list[Component],
    right_childrens: list[Component],
) -> html.Div:
    """Функция для отрисовки шапки таблицы

    Args:
        left_childrens (list[Component]): Компоненты в левой части шапки
        right_childrens (list[Component]): Компоненты в левой части шапки

    Returns:
        html.Div: шапка таблицы
    """
    return html.Div(
        children=[
            html.Div(
                children=left_childrens,
                className="table-header-left",
            ),
            html.Div(
                children=right_childrens,
                className="table-header-right",
            ),
        ],
        className="table-header",
    )
