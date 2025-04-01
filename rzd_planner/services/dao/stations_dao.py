from dataclasses import asdict, dataclass
from typing import Self

from rzd_planner.models import Stations, db


@dataclass
class StationsDTO:
    """DTO станций"""

    name: str


class StationsDAO:
    """DAO станций"""

    def save(self: Self, dto: StationsDTO) -> None:
        """Метод для сохранения станции

        Args:
            dto (StationsDTO): DTO станций
        """
        with db.session() as session:
            obj = Stations(**asdict(dto))
            session.add(obj)
            session.commit()

    def get_all(self: Self) -> list[Stations]:
        """Метод для извлечения всех станций из БД

        Returns:
            list[Stations]: типы поездов
        """
        with db.session() as session:
            models = session.query(Stations).all()

        return models
