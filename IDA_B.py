# PHESUDOCODE
#  functionIDAStar(problem): 
#     threshold← h(problem.initial_state) 
#     while True: 
#         temp← Search(problem.initial_state, 0, threshold) 
#         if temp == FOUND:
#             return solution 
#         if temp == ∞: 
#             return failure 
#         threshold ← temp 

# functionSearch(node, g, threshold):
#     f ← g + h(node) 
#     if f > threshold: 
#         return f 
#     if problem.is_goal(node): 
#         return FOUND 
#     min_exceed← ∞ 
#     for child in expand(node, problem): 
#         temp← Search(child, g + cost(node, child), threshold) 
#             if temp == FOUND: 
#                 return FOUND 
#             if temp< min_exceed: 
#                 min_exceed ← temp 
#     return min_exceed

from datagraph3 import graph, h_values, start, goal


def is_goal(node, goal_pos):
    return node == goal_pos


def expand(node, graph):
    return [(next_node, cost) for next_node, cost in graph[node].items()]


def h(node, goal):
    return h_values[node]

# ...existing code...

def ida_star(graph, start, goal, h_values):
    FOUND = "FOUND"
    path = [start]
    threshold = h_values[start]
    
    # Metrics tracking
    metrics = {
        "expansions": 0,
        "generated": 1,  # Count initial node
        "max_frontier": 1
    }

    while True:
        temp = search(path, 0, threshold, goal, graph, metrics)
        if temp == FOUND:
            return path, metrics
        if temp == float('inf'):
            return None, metrics
        threshold = temp

def search(path, g, threshold, goal, graph, metrics):
    FOUND = "FOUND"
    node = path[-1]
    metrics["expansions"] += 1
    
    f = g + h_values[node]
    
    if f > threshold:
        return f
    
    if node == goal:
        return FOUND

    min_exceed = float('inf')
    
    for next_node, cost in expand(node, graph):
        if next_node not in path:
            metrics["generated"] += 1
            path.append(next_node)
            metrics["max_frontier"] = max(metrics["max_frontier"], len(path))
            
            temp = search(path, g + cost, threshold, goal, graph, metrics)
            
            if temp == FOUND:
                return FOUND
            
            if temp < min_exceed:
                min_exceed = temp
                
            path.pop()
            
    return min_exceed

def visualize_path(grid, path, start_pos, goal_pos):
    if not path:
        print("No path to visualize.")
        return
    vis_grid = [list(row) for row in grid]
    for r, c in path:
        if (r, c) != start_pos and (r, c) != goal_pos:
            vis_grid[r][c] = '*'
    sr, sc = start_pos
    gr, gc = goal_pos
    vis_grid[sr][sc] = 'S'
    vis_grid[gr][gc] = 'G'
    for row in vis_grid:
        print(" ".join(map(str, row)))


if __name__ == "__main__":
    
    print("Solving Graph Problem with IDA*...")
    print(f"Start: {start}, Goal: {goal}\n")
    
    solution_path = ida_star(graph, start, goal, h_values)

    if solution_path:
        print("\n--- Solution Found! ---")
        print(f"Path length: {len(solution_path) - 1} moves")
        print("Path:", " -> ".join(solution_path))
        print(f"Total cost: {sum(graph[solution_path[i]][solution_path[i+1]] for i in range(len(solution_path)-1))}")
    else:
        print("\nNo solution found.")