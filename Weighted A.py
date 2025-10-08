
import Grid
import queue
import heapq

problema=Grid.grid

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
    def __init__(self,grid):
        self.grid=grid
        self.rows=len(grid)
        self.cols=len(grid[0])
        self.initial_state=self.find_symbol('S')
        self.final_state=self.find_symbol('G')
    
    def find_symbol(self,symbol):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j] == symbol:
                    return(i,j)
        return None
    

    def is_goal(self,state):
        return state==self.final_state
    

    def heuristic(self,state):
        gx,gy = self.final_state
        x,y = state
        return abs(gx-x)+ abs(gy-y)
    
    def get_nextNodes(self,state):
        nextNodes= []
        legalMovements=[(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in legalMovements:
            x,y=state
            nx,ny = x+dx, y+dy

            if 0<= nx < self.rows and 0<=ny < self.cols:
                if self.grid[nx][ny]!='X':
                    nextNodes.append(((nx,ny),1))
        return nextNodes
    
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
