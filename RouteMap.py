import networkx as nx
from enum import Enum, auto


def routes_of_distance(
    G, source, distance, route="", cumulative=False, use_weights=False
):
    """Find all unique routes of a given distance in a network

    Parameters
    ----------
    G : networkx.DiGraph
        Weighted directed network containing one-way tracks
    source : str
        Starting stop
    distance : int
        Maximum distance along route
    route : str, optional
        Route travelled to reach current source node (default is '')
    cumulative : bool, optional
        Only returns routes matching the exact distance if False, also returns shorter routes if True (default is False)
    use_weights : bool, optional
        Uses edge weights to measure distance if True, otherwise uses number of stops (default is False)

    Returns
    -------
    List
        A list of strings containing found routes
    """
    if distance == 0:
        return {route + source}
    route += source
    routes = {route} if cumulative else set()
    for n in G.successors(source):
        decrement = G[source][n]["weight"] if use_weights else 1
        new_distance = distance - decrement
        if new_distance >= 0:
            new_routes = routes_of_distance(
                G,
                n,
                new_distance,
                route=route,
                cumulative=cumulative,
                use_weights=use_weights,
            )
            routes = routes | new_routes
    return {route for route in routes if len(route) > 1}


class RouteMap:
    """
    A class used to represent a railroad network


    Attributes
    ----------
    G : networkx.DiGraph
        Weighted directed network containing one-way tracks

    Methods
    -------
        initialize_graph(input_file_path)
                Constructs network from input file
    find_route_length(route_string)
        Calculates distance along a route
    find_number_routes(source, target, distance, distance_type)
        Calculates the number of routes of a given distance between two stops
    find_shortest_route(source, target)
        Calculates the distance along the shortest route between two stops
    """

    class DistanceType(Enum):
        """A class used to indicate the correct distance measurement"""

        MAX_DISTANCE = auto()
        MAX_STOPS = auto()
        EXACT_STOPS = auto()

    def __init__(self):
        self.G = nx.DiGraph()

    def initialize_graph(self, input_file_path):
        """Constructs network from input file

        Parameters
        ----------
        input_file_path : str
            Path to text file containing an edgelist of the railroad network
        """
        with open(input_file_path, "r") as input_file:
            for line in input_file:
                # Excpects single character stations
                source = line[0]
                target = line[1]
                distance = int(line[2:-1])
                self.G.add_edge(source, target, weight=distance)

    def find_route_length(self, route_string):
        """Calculates distance along a route

        Parameters
        ----------
        route_string : str
            String containing route, for example: 'AEBCD'

        Returns
        -------
        int
            Total distance travelled if route exists
        str
            'NO SUCH ROUTE' if route does not exist
        """
        total_distance = 0
        for stop_num in range(len(route_string) - 1):
            try:
                source = route_string[stop_num]
                target = route_string[stop_num + 1]
                total_distance += self.G[source][target]["weight"]
            except:
                return "NO SUCH ROUTE"
        return total_distance

    def find_number_routes(self, source, target, distance, distance_type):
        """Calculates the number of routes of a given distance between two stops

        Parameters
        ----------
        source : str
            Starting stop
        target : str
            Final stop
        distance : int
            Maximum distance along route
        distance_type : RouteMap.DistanceType
            Indicates whether the maximum distance is cumulative and whether to measure in number of stops or distance travelled

        Raises
        ------
        ValueError
            If an unknown distance type is given

        Returns
        -------
        int
            Total number of routes found
        """
        # Find all routes matching distance
        all_routes = list()
        if distance_type == RouteMap.DistanceType.MAX_STOPS:
            all_routes = routes_of_distance(
                self.G, source, distance, cumulative=True, use_weights=False
            )
        elif distance_type == RouteMap.DistanceType.EXACT_STOPS:
            all_routes = routes_of_distance(
                self.G, source, distance, cumulative=False, use_weights=False
            )
        elif distance_type == RouteMap.DistanceType.MAX_DISTANCE:
            all_routes = routes_of_distance(
                self.G, source, distance, cumulative=True, use_weights=True
            )
        else:
            raise ValueError

        # Find routes that reach given target
        routes_to_target = [route for route in all_routes if route[-1] == target]
        return len(routes_to_target)

    def find_shortest_route(self, source, target):
        """Calculates the distance along the shortest route between two stops

        Parameters
        ----------
        source : str
            Starting stop
        target : str
            Final stop

        Returns
        -------
        int
            Distance travelled along shortest route if route exists
        str
            'NO SUCH ROUTE' if route does not exist
        """
        if not nx.has_path(self.G, source, target):
            return "NO SUCH ROUTE"

        if source != target:
            return nx.shortest_path_length(
                self.G, source=source, target=target, weight="weight"
            )

        # If source == target, calculate shortest path from each successor
        distance = float("inf")
        for n in self.G.successors(source):
            try:
                curr_distance = self.G[source][n]["weight"] + nx.shortest_path_length(
                    self.G, source=n, target=target, weight="weight"
                )
            except:
                continue
            if curr_distance < distance:
                distance = curr_distance
        if distance == float("inf"):
            return "NO SUCH ROUTE"
        return int(distance)
