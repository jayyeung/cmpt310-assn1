from model.search_sim import SearchSim

# Greedy Best First Search
class BFSSim(SearchSim):
    def getHeuristic(self, pos):
        pos1 = pos; pos2 = self.end_pos
        # manhattan distance
        x1 = pos1[0]; x2 = pos2[0]
        y1 = pos1[1]; y2 = pos2[1]
        return abs(x1-x2) + abs(y1-y2) 

    def getCost(self, next_pos):
        heuristic = self.getHeuristic(next_pos) # h(n) 
        return heuristic 


# A* Search
class AStarSim(BFSSim):
    def getCost(self, next_pos):
        totalCost = (self.cur_cost + self.getMoveCost(next_pos)) # g(n)
        heuristic = self.getHeuristic(next_pos) # h(n)
        return totalCost + heuristic


# Running the searches
testData = './data/assn1.txt'      

print('\n\nBFS SEARCH\n------------')
bfsSim = BFSSim(testData)
bfsSim.simulate()

print('\n\nA* SEARCH\n------------')
aStarSim = AStarSim(testData) 
aStarSim.simulate() 

  