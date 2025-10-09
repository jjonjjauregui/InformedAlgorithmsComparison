import Grid
from queue import PriorityQueue

problem = Grid.grid

# === FUNCIONES AUXILIARES ===
def find_position(problem, value):
    for i, row in enumerate(problem):
        for j, val in enumerate(row):
            if val == value:
                return (i, j)
    return None

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def get_neighbors(pos, problem):
    moves = [(-1,0),(1,0),(0,-1),(0,1)]
    neighbors = []
    rows, cols = len(problem), len(problem[0])
    for dx, dy in moves:
        nx, ny = pos[0] + dx, pos[1] + dy
        if 0 <= nx < rows and 0 <= ny < cols and problem[nx][ny] != 'X':
            neighbors.append((nx, ny))
    return neighbors

# === GREEDY BEST-FIRST SEARCH SIN _ ===
def greedy_best_first_search(problem):
    start = find_position(problem, 'S')
    goal = find_position(problem, 'G')
    
    frontier = PriorityQueue()
    frontier.put((heuristic(start, goal), start))
    came_from = {start: None}
    explored = set()

    while not frontier.empty():
        priority, current = frontier.get()  # ahora guardamos la prioridad explícitamente

        if current == goal:
            break

        explored.add(current)

        for neighbor in get_neighbors(current, problem):
            if neighbor not in explored and neighbor not in came_from:
                came_from[neighbor] = current
                frontier.put((heuristic(neighbor, goal), neighbor))

    # reconstruir camino
    if goal not in came_from:
        return None

    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path

# === EJECUCIÓN ===
path = greedy_best_first_search(problem)

if path:
    for (x, y) in path:
        if problem[x][y] not in ('S', 'G'):
            problem[x][y] = '.'

    for fila in problem:
        print(' '.join(fila))
else:
    print("No se encontró un camino.")


