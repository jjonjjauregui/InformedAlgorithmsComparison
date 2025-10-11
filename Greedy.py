import datagraph1
import datagraph2
import datagraph3
import Grid
import queue
import heapq

#problema=datagraph1.graph
#problema=datagraph2.graph
problema=datagraph3.graph


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
    # def __init__(self,grid):
    #     self.grid=grid
    #     self.rows=len(grid)
    #     self.cols=len(grid[0])
    #     self.initial_state=self.find_symbol('S')
    #     self.final_state=self.find_symbol('G')

    #def __init__(self, graph,h_values,initial_state='S', final_state='G'): (Adecuar al inicio y al final de cada graph)
    def __init__(self, graph,h_values,initial_state='S', final_state='Z'):
        self.graph = graph
        self.h_values = h_values
        self.initial_state = initial_state
        self.final_state = final_state

    
    # def find_symbol(self,symbol):
    #     for i in range(self.rows):
    #         for j in range(self.cols):
    #             if self.grid[i][j] == symbol:
    #                 return(i,j)
    #     return None
    

    def is_goal(self,state):
        return state==self.final_state
    

    def heuristic(self,state):
        # gx,gy = self.final_state
        # x,y = state
        # return abs(gx-x)+ abs(gy-y)
        return self.h_values[state]
    
    
    def get_nextNodes(self,state):
        # nextNodes= []
        # legalMovements=[(-1, 0), (1, 0), (0, -1), (0, 1)]
        # for dx, dy in legalMovements:
        #     x,y=state
        #     nx,ny = x+dx, y+dy

        #     if 0<= nx < self.rows and 0<=ny < self.cols:
        #         if self.grid[nx][ny]!='X':
        #             nextNodes.append(((nx,ny),1))
        # return nextNodes
        return list(self.graph[state].items())
    
def final_path(node):
    path=[]
    while node:
        path.append(node.state)
        node=node.parent
    return path[::-1]


def AStarSearch(problema,w1=1,w2=1.5):
    node=Node(problema.initial_state, None, g=0,h=problema.heuristic(problema.initial_state))
    node.f=w1*node.g+w2*node.h
    frontier = []
    heapq.heappush(frontier,(node.f,node))
    explored=set()
    while frontier:
        _,node = heapq.heappop(frontier)
        if problema.is_goal(node.state):
            return final_path(node)
        explored.add(node.state)
        for (next_state,cost) in problema.get_nextNodes(node.state):
            g=node.g+cost
            h=problema.heuristic(next_state)
            f=w1*g+w2*h
            child=Node(next_state,node,g,h)
            child.f=f
            in_frontier=any(n.state==child.state for(_,n)in frontier)
            if child.state not in explored and not in_frontier:
                heapq.heappush(frontier,(child.f,child))
            elif in_frontier:
                for i,(old_f,n) in enumerate (frontier):
                    if n.state==child.state and n.f>child.f:
                        frontier[i]=(child.f,child)
                        heapq.heapify(frontier)
                        break
    return None




#iniciar
if __name__=="__main__":
    # problema=Problema(Grid.grid)
    # path = AStarSearch(problema)

    # if path:
    #     print("Ruta:")
    #     print (path)
    #     print(f"Path length: {len(path) - 1} moves")

    # else:
    #     print("no se ha podido encontrar ninguna solucion")


    #problema=Problema(datagraph1.graph,datagraph1.h_values)
    #problema=Problema(datagraph2.graph,datagraph2.h_values)
    problema=Problema(datagraph3.graph,datagraph3.h_values)
    path = AStarSearch(problema)
    if path:
        print("Ruta:")
        print (path)
        print(f"Path length: {len(path) - 1} moves")
    else:
        print("no se ha podido encontrar ninguna solucion")