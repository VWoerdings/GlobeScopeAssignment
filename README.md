# GlobeScopeAssignment
## Files
- *assessment_input.txt*: Contains edgelist to initialize railroad network. Each edge should be on a new line and have the format [source][target][distance]. The stops should be single characters, the distance should be a positive integer.
- *RouteMap.py*: Contains the RouteMap class that calculates the solution.
- *RouteMapTest.py*: Contains the test cases from the assignment.

## Testing
To test the solution:
```sh
python RouteMapTest.py -v
```

## Design
The RouteMap class contains 3 functions:
- find_route_length(route_string)
  - Calculates distance along a route
- find_number_routes(source, target, distance, distance_type)
  - Calculates the number of routes of a given distance between two stops
  - Test cases 6, 7, and 10 are combined in this single function because of the similar logic require. The class DistanceType distinguishes between the differnt cases.
- find_shortest_route(source, target)
  - Calculates the distance along the shortest route between two stops

## Assumptions
- The network has directed edges with positive integer weights and no self-loops.
- Each stop has a unique, single letter identifier
