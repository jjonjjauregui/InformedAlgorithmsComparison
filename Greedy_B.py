from datagraph3 import graph, h_values, start, goal
from queue import PriorityQueue


def greedy_best_first_search(graph, start_node, goal_node, h_values):
    frontier = PriorityQueue()
    frontier.put((h_values[start_node], start_node))
    came_from = {start_node: None}
    explored = set()
    
    # Metrics tracking
    expansions = 0
    generated = 1  # Count initial node
    max_frontier = 1
    
    while not frontier.empty():
        _, current = frontier.get()
        expansions += 1
        
        if current == goal_node:
            break
            
        explored.add(current)
        
        for neighbor, cost in graph[current].items():
            if neighbor not in explored and neighbor not in came_from:
                generated += 1
                came_from[neighbor] = current
                frontier.put((h_values[neighbor], neighbor))
                max_frontier = max(max_frontier, frontier.qsize())
    
    # Reconstruct path
    if goal_node not in came_from:
        return None, {"expansions": expansions, "generated": generated, "max_frontier": max_frontier}
    
    path = []
    current = goal_node
    while current != start_node:
        path.append(current)
        current = came_from[current]
    path.append(start_node)
    path.reverse()
    
    return path, {"expansions": expansions, "generated": generated, "max_frontier": max_frontier}

if __name__ == "__main__":
    path = greedy_best_first_search(graph, start, goal, h_values)
    print("Path:", path)