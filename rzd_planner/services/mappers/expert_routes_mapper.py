from __future__ import annotations

from typing import Self, TypedDict, cast

from rzd_planner.models import TrainRoutes


class TrainRoutesTableType(TypedDict):
    """Структура строки таблицы маршрутов поездов"""

    id: str
    start_station: str
    end_station: str
    route_distance: float


class TrainRoutesMapper:
    """Класс для преобразования моделей маршрутов поездов в строки таблицы"""

    def model_to_table(
        self: Self, objects: list[TrainRoutes]
    ) -> list[TrainRoutesTableType]:
        """Метод для преобразования моделей маршрутов поездов в строки таблицы

        Args:
            objects (list[TrainRoutes]): Модели базы данных

        Returns:
            list[TrainRoutesTableType]: список строк таблицы на странице
        """
        result_arr = []
        for obj in objects:
            elem = {
                "id": str(obj.id),
                "start_station": obj.start_station.name,
                "end_station": obj.end_station.name,
                "route_distance": obj.distance,
            }
            result_arr.append(cast(TrainRoutesTableType, elem))

        return result_arr
