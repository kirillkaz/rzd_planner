from __future__ import annotations

from typing import Self, TypedDict, cast

from rzd_planner.models import Trains


class TrainsTableType(TypedDict):
    """Структура строки таблицы поездов"""

    id: str
    train_number: str
    train_type: str
    train_speed: str
    travel_distance: str


class TrainsMapper:
    """Класс для преобразования моделей маршрутов поездов в строки таблицы"""

    def model_to_table(self: Self, objects: list[Trains]) -> list[TrainsTableType]:
        """Метод для преобразования моделей маршрутов поездов в строки таблицы

        Args:
            objects (list[Trains]): Модели базы данных

        Returns:
            list[TrainsTableType]: список строк таблицы на странице
        """
        result_arr = []
        for obj in objects:
            elem = {
                "id": str(obj.id),
                "train_number": obj.train_number,
                "train_type": obj.train_type.name,
                "train_speed": f"от {obj.train_type.min_speed} км/ч до {obj.train_type.max_speed} км/ч",
                "travel_distance": f"от {obj.train_type.min_distance} км до {obj.train_type.max_distance} км",
            }
            result_arr.append(cast(TrainsTableType, elem))

        return result_arr
