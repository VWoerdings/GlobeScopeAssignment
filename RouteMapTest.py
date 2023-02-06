import unittest
from RouteMap import RouteMap


class RouteMapTest(unittest.TestCase):
    def setUp(self):
        input_file_path = "./assessment_input.txt"
        self.routes = RouteMap()
        self.routes.initialize_graph(input_file_path)

    def test_find_route_length(self):
        known_route_lengths = [
            ("ABC", 9),  # Test 1
            ("AD", 5),  # Test 2
            ("ADC", 13),  # Test 3
            ("AEBCD", 22),  # Test 4
            ("AED", "NO SUCH ROUTE"),  # Test 5
        ]
        for i, o in known_route_lengths:
            with self.subTest(i):
                self.assertEqual(self.routes.find_route_length(i), o)

    def test_find_number_routes(self):
        known_number_routes = [
            (("C", "C", 3, RouteMap.DistanceType.MAX_STOPS), 2),  # Test 6
            (("A", "C", 4, RouteMap.DistanceType.EXACT_STOPS), 3),  # Test 7
            (("C", "C", 30 - 1, RouteMap.DistanceType.MAX_DISTANCE), 7),  # Test 10
        ]
        for i, o in known_number_routes:
            with self.subTest(i):
                self.assertEqual(self.routes.find_number_routes(*i), o)
        return

    def test_find_shortest_route(self):
        known_shortest_routes = [
            (("A", "C"), 9),  # Test 8
            (("B", "B"), 9),  # Test 9
        ]
        for i, o in known_shortest_routes:
            with self.subTest(i):
                self.assertEqual(self.routes.find_shortest_route(*i), o)


if __name__ == "__main__":
    unittest.main()
