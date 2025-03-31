from __future__ import annotations

from typing import Final, TypedDict

from dash_extensions.enrich import html
from dash_table import DataTable

MAX_PAGE_SIZE: Final[int] = 100


class TableColumn(TypedDict):
    """Класс, описывающий структуру колонки таблицы"""

    name: str
    id: str


def render_table(
    table_id: str,
    columns_def: list[TableColumn],
    class_name: str = "default-table-block",
    row_selectable: str | None = "multi",
) -> html.Div:
    """Функция для отрисовки таблицы"""
    return html.Div(
        DataTable(
            id=table_id,
            columns=columns_def,
            page_size=MAX_PAGE_SIZE,
            editable=False,
            sort_action="native",
            sort_mode="multi",
            filter_action="native",
            row_selectable=row_selectable,
        ),
        className=class_name,
    )
