from __future__ import annotations

from typing import Self, TypedDict

from rzd_planner.models import db
from rzd_planner.services.dao import (
    ExpertRoutesDAO,
    FullRoutesDAO,
    StationsDAO,
    TrainDAO,
    TrainTravelTimesDAO,
    TrainTypeDAO,
)


class KnowledgeBaseRowType(TypedDict):
    """Структура строки таблицы страницы базы знаний"""

    knoledge_name: str
    description: str


class KnowledgeCheckService:
    """Сервис для проверки полноты базы знаний"""

    def _check_train_types(self: Self) -> KnowledgeBaseRowType:
        """Метод для проверки полноты типов поездов"""
        if not TrainTypeDAO().get_all():
            return KnowledgeBaseRowType(
                knoledge_name="Типы поездов",
                description="❌ В базе знаний нет ни одного типа поезда. ❌",
            )
        return KnowledgeBaseRowType(
            knoledge_name="Типы поездов",
            description="✅ Отклонений в полноте базы знаний не обнаружено. ✅",
        )

    def _check_stations(self: Self) -> KnowledgeBaseRowType:
        """Метод для проверки полноты станций"""
        if not StationsDAO().get_all():
            return KnowledgeBaseRowType(
                knoledge_name="Станции",
                description="❌ В базе знаний нет ни одной станции. ❌",
            )
        return KnowledgeBaseRowType(
            knoledge_name="Станции",
            description="✅ Отклонений в полноте базы знаний не обнаружено. ✅",
        )

    def _check_expert_routes(self: Self) -> KnowledgeBaseRowType:
        """Метод для проверки полноты марштутов эксперта"""
        if not ExpertRoutesDAO().get_all():
            return KnowledgeBaseRowType(
                knoledge_name="Маршруты эксперта",
                description="❌ В базе знаний нет ни одного маршрута. ❌",
            )
        return KnowledgeBaseRowType(
            knoledge_name="Маршруты эксперта",
            description="✅ Отклонений в полноте базы знаний не обнаружено. ✅",
        )

    def _check_trains(self: Self) -> KnowledgeBaseRowType:
        """Метод для проверки полноты поездов"""
        if not TrainDAO().get_all():
            return KnowledgeBaseRowType(
                knoledge_name="Поезда",
                description="❌ В базе знаний нет ни одного поезда. ❌",
            )
        return KnowledgeBaseRowType(
            knoledge_name="Поезда",
            description="✅ Отклонений в полноте базы знаний не обнаружено. ✅",
        )

    def _check_user_routes(self: Self) -> KnowledgeBaseRowType:
        """Метод для проверки полноты маршрутов пользователя"""
        if not FullRoutesDAO().get_all():
            return KnowledgeBaseRowType(
                knoledge_name="Маршруты пользователя",
                description="❌ В базе знаний нет ни одного маршрута пользователя. ❌",
            )
        return KnowledgeBaseRowType(
            knoledge_name="Маршруты пользователя",
            description="✅ Отклонений в полноте базы знаний не обнаружено. ✅",
        )

    def _check_travel_times(self: Self) -> KnowledgeBaseRowType:
        """Метод для проверки полноты времён поездок"""
        if not TrainTravelTimesDAO().get_all():
            return KnowledgeBaseRowType(
                knoledge_name="Времена поездок",
                description="❌ В базе знаний нет ни одного времени поездки. ❌",
            )
        return KnowledgeBaseRowType(
            knoledge_name="Времена поездок",
            description="✅ Отклонений в полноте базы знаний не обнаружено. ✅",
        )

    def execute(self: Self) -> list[KnowledgeBaseRowType]:
        """Метод для запуска проверки полноты базы знаний"""
        return [
            self._check_train_types(),
            self._check_stations(),
            self._check_expert_routes(),
            self._check_trains(),
            self._check_user_routes(),
            self._check_travel_times(),
        ]
