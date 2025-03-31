from logging import Logger
from typing import Self

from sqlalchemy.exc import SQLAlchemyError

from rzd_planner.config import UserRoles
from rzd_planner.models import User, db

logger = Logger(__name__)


class UserDAO:
    """DAO для работы с пользователями"""

    def get_role_by_username(self: Self, username: str) -> UserRoles:
        """Метод для извлечения роли пользователя по его имени

        Args:
            username (str): Имя пользователя

        Returns:
            UserRoles: Роль пользователя
        """
        with db.session() as session:
            try:
                user = session.query(User).filter(User.username == username).first()
            except SQLAlchemyError:
                logger.error(f"User with {username=} not exists")

            return user.role
