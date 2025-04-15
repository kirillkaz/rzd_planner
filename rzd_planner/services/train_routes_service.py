from __future__ import annotations

from typing import Self

import networkx as nx

from rzd_planner.models import TrainRoutes
from rzd_planner.services.dao.expert_routes_dao import ExpertRoutesDAO


class TrainRoutesService:
    """Сервис для получения всех маршрутов поездов"""

    def _find_all_routes(self: Self, graph: nx.DiGraph) -> list[str]:
        """Метод для поиска всех маршрутов в графе"""
        all_routes = []
        for start in graph.nodes:
            for end in graph.nodes:
                if start != end:  # Исключаем пути из вершины в саму себя
                    paths = nx.all_simple_paths(graph, source=start, target=end)
                    for path in paths:
                        all_routes.append(" -> ".join(path))
        return all_routes

    def get_train_routes(self: Self, all_routes: list[TrainRoutes]) -> list[str]:
        """Метод для получения всех маршрутов поездов"""
        Graph = nx.DiGraph()

        routes = []

        for route in all_routes:
            routes.append((route.start_station.name, route.end_station.name))

        Graph.add_edges_from(routes)

        result = self._find_all_routes(Graph)

        return result
