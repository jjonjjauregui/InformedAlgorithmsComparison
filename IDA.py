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

import Grid
from datagraph3 import graph, h_values, start, goal


def is_goal(node, goal_pos):
    return node == goal_pos


def expand(node, graph):
    return [(next_node, cost) for next_node, cost in graph[node].items()]


# def expand(node, grid):
#     neighbors = []
#     row, col = node
#     grid_rows, grid_cols = len(grid), len(grid[0])
#     moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

#     for dr, dc in moves:
#         new_row, new_col = row + dr, col + dc
#         if 0 <= new_row < grid_rows and 0 <= new_col < grid_cols:
#             if grid[new_row][new_col] == 0:
#                 neighbors.append((new_row, new_col))
#     return neighbors

# def h(node, goal_pos):
#     return abs(node[0] - goal_pos[0]) + abs(node[1] - goal_pos[1])

def h(node, goal):
    return h_values[node]

# def ida_star(grid, start_pos, goal_pos):
#     FOUND = "FOUND" 
#     path = [start_pos]
#     threshold = h(start_pos, goal_pos)
#     while True:
#         temp = search(path, 0, threshold, goal_pos, grid)
#         if temp == FOUND:
#             return path  
#         if temp == float('inf'):
#             return None  
#         threshold = temp

def ida_star(graph, start, goal, h_values):
    FOUND = "FOUND"
    path = [start]
    threshold = h_values[start]

    while True:
        temp = search(path, 0, threshold, goal, graph)
        if temp == FOUND:
            return path
        if temp == float('inf'):
            return None
        threshold = temp

# def search(path, g, threshold, goal_pos, grid):
#     FOUND = "FOUND"
#     node = path[-1] 
    
#     f = g + h(node, goal_pos)
    
#     if f > threshold:
#         return f
    
#     if is_goal(node, goal_pos):
#         return FOUND

#     min_exceed = float('inf')
    
#     for child in expand(node, grid):
#         if child not in path: 
#             path.append(child) 
#             temp = search(path, g + 1, threshold, goal_pos, grid)
            
#             if temp == FOUND:
#                 return FOUND
            
#             if temp < min_exceed:
#                 min_exceed = temp
                
#             path.pop() 
            
#     return min_exceed

def search(path, g, threshold, goal, graph):
    FOUND = "FOUND"
    node = path[-1]
    
    f = g + h_values[node]
    
    if f > threshold:
        return f
    
    if node == goal:
        return FOUND

    min_exceed = float('inf')
    
    for next_node, cost in expand(node, graph):
        if next_node not in path:
            path.append(next_node)
            temp = search(path, g + cost, threshold, goal, graph)
            
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



# if __name__ == "__main__":

#     grid_data = Grid.gridN
#     start_pos = (0, 0)
#     goal_pos = (6, 5)

#     print("Solving Grid Pathfinding with IDA* (procedural style)...")
#     print(f"Start: {start_pos}, Goal: {goal_pos}\n")
    
#     solution_path = ida_star(grid_data, start_pos, goal_pos)

#     if solution_path:
#         print("\n--- Solution Found! ---")
#         print(f"Path length: {len(solution_path) - 1} moves")
#         print("Path:", " -> ".join(map(str, solution_path)))
#         print("\n--- Visualization ---")
#         visualize_path(grid_data, solution_path, start_pos, goal_pos)
#     else:
#         print("\nNo solution found.")