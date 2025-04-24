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


class TrainOption(TypedDict):
    """Струкрута опции в dbc.Select"""

    label: str
    value: str


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

    def model_to_options(self: Self, objects: list[Trains]) -> list[TrainOption]:
        """Метод для преобразования моделей типов поездов в опции dbc.Select

        Args:
            objects (list[Trains]): Список моделей

        Returns:
            list[TrainOption]: Список опций
        """
        result_arr = []
        for obj in objects:
            elem = {
                "value": str(obj.id),
                "label": obj.train_number,
            }
            result_arr.append(cast(TrainOption, elem))

        return result_arr
