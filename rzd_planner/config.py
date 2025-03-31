import os
from dataclasses import dataclass
from enum import StrEnum


class UserRoles(StrEnum):
    EXPERT: str = "expert"
    USER: str = "user"


@dataclass
class Config:
    """Базовый класс конфигурации"""


class ProdConfig(Config):
    """Продуктовый конфиг"""

    SQLALCHEMY_DATABASE_URI: str = os.getenv("SQLALCHEMY_DATABASE_URI", "")


def init_config(config_name: str = os.getenv("CONFIG_NAME", "default")) -> Config:
    """Функция для инициализации конфигурации проекта"""
    configs = {
        "prod": ProdConfig(),
        "default": ProdConfig(),
    }

    return configs[config_name]


config = init_config()
