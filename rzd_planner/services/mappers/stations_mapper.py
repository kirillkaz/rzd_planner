from __future__ import annotations

from typing import Self, TypedDict, cast

from rzd_planner.models import Stations


class StationsTableType(TypedDict):
    """Структура строки таблицы станций"""

    id: str
    station: str


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
