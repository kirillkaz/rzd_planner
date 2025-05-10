from __future__ import annotations

from dataclasses import dataclass
from typing import Self

from sqlalchemy.exc import SQLAlchemyError

from rzd_planner.models import FullRoutes, Trains, TrainTravelTimes, db


@dataclass
class SchedulePlannerDTO:
    """DTO для планирования расписания поездов"""

    data: list[tuple[str, str, int]]


class SchedulePlannerDAO:
    """DAO для планирования расписания поездов"""

    def get_schedule_plan_records(self: Self) -> SchedulePlannerDTO:
        """Метод для получения записей для планирования расписания жп перевозок"""
        try:
            with db.session() as session:
                data = (
                    session.query(
                        Trains.train_number,
                        FullRoutes.route,
                        TrainTravelTimes.total_time,
                    )
                    .join(
                        FullRoutes,
                        FullRoutes.train_id == Trains.id,
                    )
                    .join(
                        TrainTravelTimes,
                        TrainTravelTimes.train_route_id == FullRoutes.id,
                    )
                    .all()
                )
        except SQLAlchemyError as ex:
            print(ex)
            return SchedulePlannerDTO(data=[])
        return SchedulePlannerDTO(data=data)
