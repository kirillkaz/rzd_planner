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

    def _format_duration(self: Self, seconds: int) -> tuple[int, int, int]:
        """# TODO: это надо вынести
        Фунция для преобразования секунд в кортеж (дни, часы, минуты)

        Args:
            seconds (int): время в секундах

        Returns:
            tuple[int, int, int]: кортеж (дни, часы, минуты)
        """
        days = seconds // 86400
        seconds %= 86400
        hours = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        return days, hours, minutes

    def _time_to_str(self: Self, days: int, hours: int, minutes: int) -> str:
        d = f"{days} дн. " if days else ""
        h = f"{hours} ч. " if hours else ""
        m = f"{minutes} мин. " if minutes else ""

        return d + h + m

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
            total_seconds = obj.total_time
            days, hours, minutes = self._format_duration(total_seconds)
            total_time = self._time_to_str(days=days, hours=hours, minutes=minutes)

            elem = {
                "id": str(obj.id),
                "total_time": total_time,
                "train_route": obj.full_route.route,
            }
            result_arr.append(cast(TrainTravelTimesTableType, elem))

        return result_arr
