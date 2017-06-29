import networkx as nx
from geopy.distance import great_circle

from .utils import travel_distances
from .models import Route


class RouteBuilder:
    def __init__(self, tourist):
        self.tourist = tourist
        self.starting_point = tourist.coordinates

    def build_routes(self, places):
        places_per_route = self._places_per_route()
        routes_count = len(places) // places_per_route
        groups = self._group_places(places[:routes_count], places[routes_count:])
        routes = []

        for group in groups:
            path = self._build_path(group)
            if path is not None:
                route = Route.from_path(path, self.tourist)
                routes.append(route)

        return routes

    def _group_places(self, starting_places, others):
        groups = []
        for s in starting_places:
            group = [s]
            for dest in others:
                dist = self._distance_between(s[0], dest[0])
                if dist < travel_distances[self.tourist.travel_dist]:
                    group.append((dest[0], dist))
            groups.append(group)

        return groups

    def _build_path(self, places):
        if len(places) == 0: return None

        graph = nx.Graph()
        graph.add_node(places[0][0])
        for place in places[1:]:
            graph.add_edge(places[0][0], place[0], distance=place[1])

        # add missing edges
        for i in range(1, len(places) - 2):
            for j in range(i + 1, len(places) - 1):
                origin = places[i][0]  # places is a list of tuples (Place, dist_to_tourist)
                destination = places[j][0]
                # TODO: Calculate distances using Google Maps Distance Matrix API for more accuracy.
                dist = self._distance_between(origin, destination)
                if dist < travel_distances[self.tourist.travel_dist]:
                    graph.add_edge(origin, destination, distance=dist)

        mst = nx.minimum_spanning_tree(graph, weight='distance')

        if len(mst) == 1:
            return list(mst.nodes())

        path = list(nx.all_simple_paths(mst, places[0][0], places[-1][0]))
        return path[0]

    def _distance_between(self, origin, dest):
        origin_coords = origin.coordinates['coordinates']
        destination_coords = dest.coordinates['coordinates']
        dist = great_circle(origin_coords, destination_coords)

        return dist.kilometers

    def _places_per_route(self):
        """
        Calculates how many places a route will contain, given the budget of the tourist.
         - Low budget routes includes 1 place per route
         - Moderate budget routes includes 3 places per route
         - High budget routes includes 5 places per route
        :return: The amount of places to be included in each route.
        """
        budget = self.tourist.budget
        return [1, 3, 5][budget]
