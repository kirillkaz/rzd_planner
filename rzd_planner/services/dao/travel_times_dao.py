from dataclasses import asdict, dataclass
from typing import Self

from sqlalchemy.orm import joinedload

from rzd_planner.models import TrainTravelTimes, db

type TotalSeconds = int

@dataclass
class TrainTravelTimesDTO:
    """DTO времени поездок"""

    total_time: TotalSeconds
    train_route_id: str


class TrainTravelTimesDAO:
    """DAO времени поездок"""

    def save(self: Self, dto: TrainTravelTimesDTO) -> None:
        """Метод для сохранения времени поездок

        Args:
            dto (TrainTravelTimesDTO): DTO времени поездок
        """
        with db.session() as session:
            obj = TrainTravelTimes(**asdict(dto))
            session.add(obj)
            session.commit()

    def get_all(self: Self) -> list[TrainTravelTimes]:
        """Метод для извлечения всех времени поездок из БД

        Returns:
            list[TrainTravelTimes]: временена поездок
        """
        with db.session() as session:
            models = (
                session.query(TrainTravelTimes)
                .options(joinedload(TrainTravelTimes.full_route))
                .all()
            )

        return models

    def delete(self: Self, uuid_lst: list[str]) -> None:
        """Метод для удаления времен поездок

        Args:
            uuid_lst (list[str]): список uuid записей
        """
        with db.session() as session:
            session.query(TrainTravelTimes).filter(
                TrainTravelTimes.id.in_(uuid_lst)
            ).delete(synchronize_session=False)
            session.commit()
