# ast just helps convert strings into actual parameters
from queue import PriorityQueue
from ast import literal_eval
from copy import deepcopy

# This func reads the input from /data
def getInputData(path):
    with open(path) as data:
        line = data.read().splitlines()
        return line

# SearchSim
class SearchSim:
    def __init__(self, data):
        # pre-cond: txt data given are well-formatted
        # and parameters follow the order below
        res = getInputData(data)
        self.grid_size = int(res[0])
        self.start_pos  = literal_eval(res[1])
        self.end_pos = literal_eval(res[2])
        self.grid = literal_eval(''.join(map(str, res[3:])))

        self.cur_pos = self.start_pos

    def simulate(self):
        fringe = PriorityQueue()
        checked_nodes = {}
        node_parent = {}
        self.nodes_expanded = 0

        # add start_pos to the fringe and make sure we know it's checked
        # we store it as tuples where = (f(n), [x,y])
        fringe.put((0, self.start_pos)) 
        checked_nodes[str(self.start_pos)] = True

        while (not fringe.empty()):
            current = fringe.get()
            cur_cost = self.cur_cost = current[0]
            cur_pos = self.cur_pos = current[1]
            neighbours = self.getNeighbours(cur_pos)

            # if solution is found
            if (cur_pos == self.end_pos):
                path = self.reconstructPath(node_parent)
                return self.printResults(path)

            for neighbour in neighbours:
                neighbour_i = str(neighbour)

                # if we haven't check any previous neighbours yet
                if (not neighbour_i in checked_nodes):
                    node_parent[neighbour_i] = cur_pos
                    checked_nodes[neighbour_i] = True
                    # figure out cost -- dependent on implementation
                    cost = self.getCost(neighbour)
                    fringe.put((cost, neighbour))
                    self.nodes_expanded += 1
        
        # no more fringe nodes -- no solution
        return 'ERROR: No solution found.'

    def printResults(self, path):
        print('Total nodes expanded: {}'.format(self.nodes_expanded))
        print('Path (n = {}) -> {}'.format(len(path), path))
        print('\n--------------\nDiagram\n--------------')
        # format grid to print
        grid = deepcopy(self.grid)
        for node in path: grid[node[1]][node[0]] = '⬛'
        for row in grid: print(' '.join(['{:<{sp}}'.format(ele,sp=3) for ele in row]))
            
    def reconstructPath(self, node_parent):
        path = [self.end_pos]
        current = str(self.end_pos)
        while (current in node_parent):
            current = node_parent[current]
            path.append(current)
            if (current == self.start_pos): return path[::-1]
            else: current = str(current) 

    # helper methods
    def getGridVal(self, pos):
        return self.grid[pos[1]][pos[0]]

    def getMoveCost(self, pos):
        cur_pos = self.cur_pos
        return 1 + abs(self.getGridVal(cur_pos) - self.getGridVal(pos))
    
    def getNeighbours(self, pos):
        x = pos[0]; y = pos[1]
        # neighbors = [up, right, down, left]
        neighbours = [[x, y-1], [x+1, y], [x, y+1], [x-1, y]]
        filters = lambda x : (self.isInBounds(x) and self.isWalkable(x))
        filtered_neighbours = filter(filters, neighbours)
        return list(filtered_neighbours)

    # Neighbour Filters
    def isInBounds(self, pos):
        size = self.grid_size
        return (0 <= pos[0] < size) and (0 <= pos[1] < size)

    def isWalkable(self, pos):
        return (self.getMoveCost(pos)-1) < 4

    # abstract methods
    def getCost(self, next_pos): pass

