from dataclasses import asdict, dataclass
from typing import Self

from sqlalchemy import and_
from sqlalchemy.orm import joinedload

from rzd_planner.models import Stations, TrainRoutes, db


@dataclass
class ExpertRouteDTO:
    """DTO маршрутов поездов"""

    distance: float
    start_station_id: str
    end_station_id: str


class ExpertRoutesDAO:
    """DAO маршрутов поездов"""

    def save(self: Self, dto: ExpertRouteDTO) -> None:
        """Метод для сохранения маршрута поезда

        Args:
            dto (ExpertRouteDTO): DTO маршрута поезда
        """
        with db.session() as session:
            obj = TrainRoutes(**asdict(dto))
            session.add(obj)
            session.commit()

    def get_all(self: Self) -> list[TrainRoutes]:
        """Метод для извлечения всех маршрутов поездов из БД

        Returns:
            list[Stations]: маршруты поездов
        """
        with db.session() as session:
            models = (
                session.query(TrainRoutes)
                .options(
                    joinedload(
                        TrainRoutes.start_station,
                    ),
                    joinedload(
                        TrainRoutes.end_station,
                    ),
                )
                .all()
            )

        return models

    def get_route_by_start_end(self: Self, start: str, end: str) -> TrainRoutes:
        """Метод для получения маршрута по названиям начальной и конечной станций

        Args:
            start (str): Название начальной станции
            end (str): Название конечной станции
        """

        # костыльное решение :(
        with db.session() as session:
            start_station = (
                session.query(Stations).filter(Stations.name == start).first()
            )
            end_station = session.query(Stations).filter(Stations.name == end).first()

            train_route = (
                session.query(TrainRoutes)
                .filter(
                    and_(
                        TrainRoutes.start_station_id == start_station.id,
                        TrainRoutes.end_station_id == end_station.id,
                    )
                )
                .first()
            )

            return train_route

    def delete(self: Self, uuid_lst: list[str]) -> None:
        """Метод для удаления маршрутов поездов

        Args:
            uuid_lst (list[str]): список uuid записей
        """
        with db.session() as session:
            session.query(TrainRoutes).filter(TrainRoutes.id.in_(uuid_lst)).delete(
                synchronize_session=False
            )
            session.commit()
