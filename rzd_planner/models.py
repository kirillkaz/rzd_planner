from __future__ import annotations

import uuid
from datetime import datetime
from enum import StrEnum

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from passlib.context import CryptContext
from sqlalchemy import CheckConstraint, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class OnDeleteActionType(StrEnum):
    """Тип для событий, происходящих при удалении продительской записи"""

    CASCADE: str = "CASCADE"
    SET_NULL: str = "SET NULL"
    RESTRICT: str = "RESTRICT"
    NO_ACTION: str = "NO ACTION"
    SET_DEFAULT: str = "SET_DEFAULT"


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(
    model_class=Base,
    engine_options={
        "pool_pre_ping": True,
        "connect_args": {
            "keepalives": 1,
            "keepalives_idle": 30,
            "keepalives_interval": 10,
            "keepalives_count": 5,
        },
    },
)


_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class FlaskMigrateUser(UserMixin):
    """модель пользователя"""

    def __init__(self, username: str) -> None:
        """конструктор модели пользователя

        Args:
            username (str): имя пользователя
        """
        self.id = username


class User(db.Model):
    """Модель пользователя"""

    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid1)
    username: Mapped[str] = mapped_column(String(30), unique=True)
    password_hash: Mapped[str] = mapped_column()
    role: Mapped[str] = mapped_column(nullable=False)

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, password: str):
        """Хеширует пароль и сохраняет его в password_hash."""
        self.password_hash = _pwd_context.hash(password)

    def verify_password(self, password: str) -> bool:
        """Проверяет, соответствует ли пароль хэшу."""
        return _pwd_context.verify(password, self.password_hash)


class TrainTypes(db.Model):
    """Модель типов поездов"""

    __tablename__ = "train_types"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid1)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    min_speed: Mapped[float] = mapped_column(nullable=False)
    max_speed: Mapped[float] = mapped_column()
    min_distance: Mapped[float] = mapped_column(nullable=False)
    max_distance: Mapped[float] = mapped_column()

    trains: Mapped[list["Trains"]] = relationship(back_populates="train_type")

    __table_args__ = (
        CheckConstraint(
            "min_speed > 0.0",
            name="min_speed_range_constraint",
        ),
        CheckConstraint(
            "max_speed > min_speed",
            name="max_speed_range_constraint",
        ),
        CheckConstraint(
            "min_distance > 0.0",
            name="min_distance_range_constraint",
        ),
        CheckConstraint(
            "max_distance > min_distance",
            name="max_distance_range_constraint",
        ),
    )


class Trains(db.Model):
    """Модель поездов"""

    __tablename__ = "trains"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid1)
    train_number: Mapped[str] = mapped_column(String(5), unique=True, nullable=False)

    train_type_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "train_types.id",
            ondelete=str(OnDeleteActionType.CASCADE),
        ),
        nullable=False,
    )

    train_type: Mapped["TrainTypes"] = relationship(back_populates="trains")


class FullRoutes(db.Model):
    """Модель полных маршрутов следования"""

    __tablename__ = "full_routes"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid1)
    route: Mapped[str] = mapped_column(unique=True, nullable=False)

    train_travel_times: Mapped[list["TrainTravelTimes"]] = relationship(
        back_populates="full_route"
    )


class TrainTravelTimes(db.Model):
    """Модель времени поездок на маршрутах"""

    __tablename__ = "train_travel_times"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid1)
    start_date: Mapped[datetime] = mapped_column(nullable=False)
    end_date: Mapped[datetime] = mapped_column(nullable=False)

    train_route_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "full_routes.id",
            ondelete=str(OnDeleteActionType.CASCADE),
        ),
        nullable=False,
        unique=True,
    )

    full_route: Mapped["FullRoutes"] = relationship(back_populates="train_travel_times")

    __table_args__ = (
        CheckConstraint(
            "start_date != end_date",
            name="dates_not_equal_constraint",
        ),
        CheckConstraint(
            "start_date < end_date",
            name="end_date_higher_start_date_constraint",
        ),
    )


class TrainRoutes(db.Model):
    """Модель маршрутов поездок"""

    __tablename__ = "train_routes"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid1)
    distance: Mapped[float] = mapped_column(nullable=False)

    start_station_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "stations.id",
            ondelete=str(OnDeleteActionType.CASCADE),
        ),
        nullable=False,
    )
    end_station_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "stations.id",
            ondelete=str(OnDeleteActionType.CASCADE),
        ),
        nullable=False,
    )

    start_station: Mapped["Stations"] = relationship(
        back_populates="routes_as_start",
        foreign_keys=[start_station_id],
    )
    end_station: Mapped["Stations"] = relationship(
        back_populates="routes_as_end",
        foreign_keys=[end_station_id],
    )

    __table_args__ = (
        CheckConstraint(
            "start_station_id != end_station_id", name="stations_not_equal_constraint"
        ),
        CheckConstraint("distance > 0.0", name="distance_range_constraint"),
        UniqueConstraint(
            "start_station_id",
            "end_station_id",
            name="start_end_stations_unique_constraint",
        ),
    )


class Stations(db.Model):
    """Модель станций"""

    __tablename__ = "stations"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid1)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)

    routes_as_start: Mapped[list["TrainRoutes"]] = relationship(
        back_populates="start_station",
        foreign_keys="[TrainRoutes.start_station_id]",
    )
    routes_as_end: Mapped[list["TrainRoutes"]] = relationship(
        back_populates="end_station",
        foreign_keys="[TrainRoutes.end_station_id]",
    )
