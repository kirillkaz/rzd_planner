from __future__ import annotations

from typing import Self, TypedDict, cast

from rzd_planner.models import Stations


class StationsTableType(TypedDict):
    """Структура строки таблицы станций"""

    id: str
    station: str


class StationsOption(TypedDict):
    """Струкрута опции в dbc.Select"""

    label: str
    value: str


class StationsMapper:
    """Класс для преобразования моделей станций в строки таблицы"""

    def model_to_table(self: Self, objects: list[Stations]) -> list[StationsTableType]:
        """Метод для преобразования моделей станций в строки таблицы

        Args:
            objects (list[Stations]): Модели базы данных

        Returns:
            list[StationsTableType]: список строк таблицы на странице
        """
        result_arr = []
        for obj in objects:
            elem = {
                "id": str(obj.id),
                "station": obj.name,
            }
            result_arr.append(cast(StationsTableType, elem))

        return result_arr

    def model_to_options(self: Self, objects: list[Stations]) -> list[StationsOption]:
        """Метод для преобразования моделей станций в опции dbc.Select

        Args:
            objects (list[Stations]): Список моделей

        Returns:
            list[StationsOption]: Список опций
        """
        result_arr = []
        for obj in objects:
            elem = {
                "value": str(obj.id),
                "label": obj.name,
            }
            result_arr.append(cast(StationsOption, elem))

        return result_arr
