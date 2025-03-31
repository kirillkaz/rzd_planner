from typing import Self

from flask import session
from flask_login import current_user, login_user

from rzd_planner.app import app, login_manager
from rzd_planner.models import FlaskMigrateUser, User, db


@login_manager.user_loader
def load_user(username: str) -> FlaskMigrateUser:
    """Функция для загрузки пользователя по идентификатору пользователя.

    Args:
        username (str): имя пользователя

    Returns:
        FlaskMigrateUser: модель пользователя
    """
    return FlaskMigrateUser(username)


class AuthService:
    def verify_user(self: Self, username: str, pwd: str) -> bool:
        """Функция для загрузки пользователя по идентификатору пользователя.

        Args:
            username (str): имя пользователя

        Returns:
            bool: Флаг (смог ли пользователь авторизоваться)
        """
        with app.server.app_context(), db.session() as session:
            user: User = session.query(User).filter(User.username == username).first()
            if user.verify_password(pwd):
                return True
        return False

    def authorize(self: Self, username: str, pwd: str) -> bool:
        """Метод для авторизации пользователя

        Args:
            username (str): Имя пользователя
            pwd (str): Пароль

        Returns:
            bool: Флаг (вошел пользователь или нет)
        """
        if self.verify_user(username, pwd):
            user = load_user(username)
        else:
            return False
        if user:
            login_user(user)
            session["username"] = current_user.get_id()
            return True
        return False
