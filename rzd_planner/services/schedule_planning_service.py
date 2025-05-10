from __future__ import annotations

from datetime import datetime, timedelta
from typing import Self, TypedDict

import pandas as pd

from rzd_planner.services.dao.schedule_planner_dao import (
    SchedulePlannerDAO,
    SchedulePlannerDTO,
)


class PlannerRecord(TypedDict):
    train_num: str
    route: str
    start_date: datetime
    end_date: datetime


class SchedulePlanner:
    """Класс-планировщик расписания поездов"""

    def _get_planner_records(
        self: Self,
        schedule_data: SchedulePlannerDTO,
        start_date: datetime,
        end_date: datetime,
    ) -> list[PlannerRecord]:
        """Метод для получения записей отчёта планировщика

        Args:
            schedule_data (SchedulePlannerDTO): Данные для планирования расписания жд поездок
            start_date (datetime): Начальная дата построения отчёта
            end_date (datetime): Конечная дата построения отчёта

        Returns:
            list[PlannerRecord]: Список записей отчёта
        """
        data = schedule_data.data
        result_records = []
        for record in data:
            train_num, route, travel_time_sec = record
            tmp_date = start_date
            while tmp_date < end_date:
                result_records.append(
                    PlannerRecord(
                        train_num=train_num,
                        route=route,
                        start_date=tmp_date,
                        end_date=tmp_date + timedelta(seconds=travel_time_sec),
                    )
                )
                tmp_date += timedelta(seconds=travel_time_sec)
        return result_records

    def _result_preprocessing(self: Self, df: pd.DataFrame) -> pd.DataFrame:
        """Метод для предобработки составленного расписания жд перевозок

        Args:
            df (pd.DataFrame):

        Returns:
            pd.DataFrame: Предобработанное расписание жд перевозок
        """
        df = df.sort_values("start_date", ascending=True)

        df["start_date"] = df["start_date"].dt.strftime("%d.%m.%Y %H:%M")
        df["end_date"] = df["end_date"].dt.strftime("%d.%m.%Y %H:%M")

        df = df.rename(
            columns={
                "train_num": "Номер поезда",
                "route": "Маршрут поездки",
                "start_date": "Дата отправления",
                "end_date": "Дата прибытия",
            }
        )
        return df

    def execute(self: Self, start_date: datetime, end_date: datetime) -> pd.DataFrame:
        """Метод для получения расписания железнодорожных перевозок

        Args:
            start_date (datetime): Дата от которой начинается составления расписания
            end_date (datetime): Дата которой оканчивается составления расписания

        Returns:
            pd.DataFrame: Расписание жд перевозок
        """
        schedule_data = SchedulePlannerDAO().get_schedule_plan_records()
        planner_records = self._get_planner_records(
            schedule_data=schedule_data,
            start_date=start_date,
            end_date=end_date,
        )
        df = pd.DataFrame(planner_records)
        df = self._result_preprocessing(df)
        return df
