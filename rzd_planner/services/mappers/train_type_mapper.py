from __future__ import annotations

from typing import Self, TypedDict, cast

from rzd_planner.models import TrainTypes


class TrainTypeTable(TypedDict):
    """Структура строки таблицы типов поездов"""

    id: str
    train_type: str
    speed: str
    travel_distance: str


class TrainTypeMapper:
    """Класс для преобразования моделей типов поездов в строки таблицы"""

    def model_to_table(self: Self, objects: list[TrainTypes]) -> list[TrainTypeTable]:
        """Метод для преобразования моделей типов поездов в строки таблицы

        Args:
            objects (list[TrainTypes]): Модели базы данных

        Returns:
            list[TrainTypeTable]: список строк таблицы на странице
        """
        result_arr = []
        for obj in objects:
            elem = {
                "id": str(obj.id),
                "train_type": obj.name,
                "speed": f"от {obj.min_speed} км/ч до {obj.max_speed} км/ч",
                "travel_distance": f"от {obj.min_distance} км до {obj.max_distance} км",
            }
            result_arr.append(cast(TrainTypeTable, elem))

        return result_arr
