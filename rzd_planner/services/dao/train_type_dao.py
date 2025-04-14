from dataclasses import asdict, dataclass
from typing import Self

from rzd_planner.models import TrainTypes, db


@dataclass
class TrainTypeDTO:
    """DTO типов поездов"""

    name: str
    min_speed: float
    max_speed: float
    min_distance: float
    max_distance: float


class TrainTypeDAO:
    """DAO типов поездов"""

    def save(self: Self, dto: TrainTypeDTO) -> None:
        """Метод для сохранения типа поездов

        Args:
            dto (TrainTypeDTO): DTO типов поездов
        """
        with db.session() as session:
            obj = TrainTypes(**asdict(dto))
            session.add(obj)
            session.commit()

    def get_all(self: Self) -> list[TrainTypes]:
        """Метод для извлечения всех типов поездов из БД

        Returns:
            list[TrainTypes]: типы поездов
        """
        with db.session() as session:
            models = session.query(TrainTypes).all()

        return models

    def delete(self: Self, uuid_lst: list[str]) -> None:
        """Метод для удаления типов поездов

        Args:
            uuid_lst (list[str]): список uuid записей
        """
        with db.session() as session:
            session.query(TrainTypes).filter(TrainTypes.id.in_(uuid_lst)).delete(synchronize_session=False)
            session.commit()
