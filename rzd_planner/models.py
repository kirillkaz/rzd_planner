from uuid import UUID

from flask_sqlalchemy import SQLAlchemy
from passlib.context import CryptContext
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


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


class User(db.Model):
    """Модель пользователя"""

    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str] = mapped_column()

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
