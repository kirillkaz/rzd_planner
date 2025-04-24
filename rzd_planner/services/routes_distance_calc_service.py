from typing import Self

from rzd_planner.services.dao import ExpertRoutesDAO


class RoutesDistanceCalc:
    """Сервис для подсчёта дистанции маршрутов поездов"""

    def _get_routes(self: Self, route: str) -> list[dict[str, float]]:
        """Метод для получения списка станций из маршрута"""
        stations = route.split(" -> ")
        routes = []
        for i in range(len(stations) - 1):
            routes.append({"start": stations[i], "end": stations[i + 1]})

        return routes

    def calc_distance(self: Self, route: str) -> float:
        """Метод для подсчёта дистанции маршрутов поездов"""
        routes = self._get_routes(route)

        distance = 0.0
        dao = ExpertRoutesDAO()
        for elem in routes:
            distance += dao.get_route_by_start_end(
                start=elem["start"], end=elem["end"]
            ).distance

        return distance
