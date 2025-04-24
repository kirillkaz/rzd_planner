from dataclasses import asdict, dataclass
from typing import Self

from sqlalchemy.orm import joinedload

from rzd_planner.models import FullRoutes, db


@dataclass
class FullRoutesDTO:
    """DTO полных маршрутов"""

    route: str
    train_id: str
    distance: float


class FullRoutesDAO:
    """DAO полных маршрутов"""

    def save(self: Self, dto: FullRoutesDTO) -> None:
        """Метод для сохранения полных маршрутов

        Args:
            dto (FullRoutesDTO): DTO полных маршрутов
        """
        with db.session() as session:
            obj = FullRoutes(**asdict(dto))
            session.add(obj)
            session.commit()

    def get_all(self: Self) -> list[FullRoutes]:
        """Метод для извлечения всех полных маршрутов из БД

        Returns:
            list[FullRoutes]: типы поездов
        """
        with db.session() as session:
            models = (
                session.query(FullRoutes).options(joinedload(FullRoutes.trains)).all()
            )

        return models

    def delete(self: Self, uuid_lst: list[str]) -> None:
        """Метод для удаления полных маршрутов

        Args:
            uuid_lst (list[str]): список uuid записей
        """
        with db.session() as session:
            session.query(FullRoutes).filter(FullRoutes.id.in_(uuid_lst)).delete(
                synchronize_session=False
            )
            session.commit()
