from __future__ import annotations

from typing import Self, TypedDict, cast

from rzd_planner.models import FullRoutes


class FullRoutesTableType(TypedDict):
    """Структура строки таблицы поездов"""

    id: str
    route: str


class FullRouteOption(TypedDict):
    """Струкрута опции в dbc.Select"""

    label: str
    value: str


class FullRoutesMapper:
    """Класс для преобразования моделей полных маршрутов поездов в строки таблицы"""

    def model_to_table(
        self: Self, objects: list[FullRoutes]
    ) -> list[FullRoutesTableType]:
        """Метод для преобразования моделей полных маршрутов поездов в строки таблицы

        Args:
            objects (list[FullRoutes]): Модели базы данных

        Returns:
            list[FullRoutesTableType]: список строк таблицы на странице
        """
        result_arr = []
        for obj in objects:
            elem = {
                "id": str(obj.id),
                "route": obj.route,
            }
            result_arr.append(cast(FullRoutesTableType, elem))

        return result_arr

    def str_to_options(
        self: Self, objects: list[str]
    ) -> list[FullRouteOption]:
        """Метод для преобразования строк полных маршрутов в опции dbc.Select

        Args:
            objects (list[str]): Список моделей

        Returns:
            list[FullRouteOption]: Список опций
        """
        result_arr = []
        for obj in objects:
            elem = {
                "value": obj,
                "label": obj,
            }
            result_arr.append(cast(FullRouteOption, elem))

        return result_arr
