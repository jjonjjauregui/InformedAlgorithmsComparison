from datagraph3 import graph, h_values, start, goal
import heapq

class Node:
    def __init__(self,state,parent=None,g=0,h=0):
        self.state=state
        self.parent=parent
        self.g=g
        self.h=h
        self.f=0

    def __lt__(self, other):
        return self.f < other.f

class Problema:
    def __init__(self, graph,h_values,initial_state='S', final_state='Z'):
        self.graph = graph
        self.h_values = h_values
        self.initial_state = initial_state
        self.final_state = final_state
   
    def is_goal(self,state):
        return state==self.final_state
   
    def heuristic(self,state):
        return self.h_values[state]
   
    def get_nextNodes(self,state):
        return list(self.graph[state].items())
   
def final_path(node):
    path=[]
    while node:
        path.append(node.state)
        node=node.parent
    return path[::-1]


def AStarSearch(problema, w1=1, w2=1.5):
    node = Node(problema.initial_state, None, g=0, h=problema.heuristic(problema.initial_state))
    node.f = w1*node.g + w2*node.h
    frontier = []
    heapq.heappush(frontier,(node.f,node))
    explored = set()
   
    # Metrics tracking
    expansions = 0
    generated = 1  # Count initial node
    max_frontier = 1
   
    while frontier:
        _,node = heapq.heappop(frontier)
        expansions += 1
       
        if problema.is_goal(node.state):
            path = final_path(node)
            return path, {
                "expansions": expansions,
                "generated": generated,
                "max_frontier": max_frontier
            }
           
        explored.add(node.state)
       
        for (next_state,cost) in problema.get_nextNodes(node.state):
            generated += 1
            g = node.g + cost
            h = problema.heuristic(next_state)
            f = w1*g + w2*h
            child = Node(next_state,node,g,h)
            child.f = f
           
            in_frontier = any(n.state==child.state for(_,n) in frontier)
            if child.state not in explored and not in_frontier:
                heapq.heappush(frontier,(child.f,child))
                max_frontier = max(max_frontier, len(frontier))
               
            elif in_frontier:
                for i,(old_f,n) in enumerate(frontier):
                    if n.state==child.state and n.f>child.f:
                        frontier[i] = (child.f,child)
                        heapq.heapify(frontier)
                        break
                       
    return None, {"expansions": expansions, "generated": generated, "max_frontier": max_frontier}

def weighted_a_star_search(graph, start, goal, h_values, weight=1.5):
    problema = Problema(graph, h_values, start, goal)
    path_and_metrics = AStarSearch(problema, w1=1, w2=weight)
    if path_and_metrics:
        path, metrics = path_and_metrics
        cost = sum(graph[path[i]][path[i+1]] for i in range(len(path)-1)) if path else float('inf')
        return path, cost, metrics
    return [], float('inf'), {"expansions": 0, "generated": 0, "max_frontier": 0}

if __name__=="__main__":
    path, cost, metrics = weighted_a_star_search(graph, start, goal, h_values)
    if path:
        print("Ruta:")
        print(path)
        print(f"Path length: {len(path) - 1} moves")
        print(f"Total cost: {cost}")
        print("Métricas:", metrics)
    else:
        print("no se ha podido encontrar ninguna solucion")