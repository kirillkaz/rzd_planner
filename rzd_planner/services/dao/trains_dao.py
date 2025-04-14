from dataclasses import asdict, dataclass
from typing import Self

from sqlalchemy.orm import joinedload

from rzd_planner.models import Trains, db


@dataclass
class TrainDTO:
    """DTO поездов"""

    train_number: str
    train_type_id: str


class TrainDAO:
    """DAO поездов"""

    def save(self: Self, dto: TrainDTO) -> None:
        """Метод для сохранения поездов

        Args:
            dto (TrainDTO): DTO поездов
        """
        with db.session() as session:
            obj = Trains(**asdict(dto))
            session.add(obj)
            session.commit()

    def get_all(self: Self) -> list[Trains]:
        """Метод для извлечения всех поездов из БД

        Returns:
            list[Trains]: поезда
        """
        with db.session() as session:
            models = (
                session.query(Trains)
                .options(
                    joinedload(
                        Trains.train_type,
                    )
                )
                .all()
            )

        return models
    
    def delete(self: Self, uuid_lst: list[str]) -> None:
        """Метод для удаления поездов

        Args:
            uuid_lst (list[str]): список uuid записей
        """
        with db.session() as session:
            session.query(Trains).filter(Trains.id.in_(uuid_lst)).delete(
                synchronize_session=False
            )
            session.commit()
