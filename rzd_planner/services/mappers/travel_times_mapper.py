from __future__ import annotations

from datetime import datetime
from typing import Self, TypedDict, cast

from rzd_planner.models import TrainTravelTimes


class TrainTravelTimesTableType(TypedDict):
    """Структура строки таблицы времен поездок"""

    id: str
    start_date: datetime
    end_date: datetime
    train_route: str


class TrainTravelTimesMapper:
    """Класс для преобразования моделей времен поездок в строки таблицы"""

    def model_to_table(
        self: Self, objects: list[TrainTravelTimes]
    ) -> list[TrainTravelTimesTableType]:
        """Метод для преобразования моделей времен поездок в строки таблицы

        Args:
            objects (list[TrainTravelTimes]): Модели базы данных

        Returns:
            list[TrainTravelTimesTableType]: список строк таблицы на странице
        """
        result_arr = []
        for obj in objects:
            elem = {
                "id": str(obj.id),
                "start_date": obj.start_date,
                "end_date": obj.end_date,
                "train_route": obj.full_route.route,
            }
            result_arr.append(cast(TrainTravelTimesTableType, elem))

        return result_arr
