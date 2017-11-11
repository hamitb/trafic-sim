class Map(object):
    def  __init__(self):
        '''create an empty map'''
    def addNode(self, id, x, y):
        '''create a vertice at (x,y) with given id'''
    def deleteNode(self, id):
        '''delete the vertice with given id. All edges connecting the vertice are also deleted'''
    def addRoad(self, id1, id2, nlanes = 1, bidir = True):
        ''' add an edge from id1 to id2. Number of lanes is set for
            each edge and if bidir is True another edge in opposite
            direction is also created. '''
    def deleteRoad(self, id1, id2, bidir = True):
        '''delete the edge between id1 and id2. If bidir is True,
            the edge in opposite direction is also deleted.'''

    def getShortestPath(self,id1,id2):
        '''The list of edges in the shortest path from id1 and id2 is
            returned as a list of tuples. (You can use Floyd-Warshall
            algorithm to calculate all shortest paths when this is
            called for the first time, then use cached value as long as
            Map is not changed)'''
    def saveMap(self, name):
        '''Save map with given name from database'''
    def deleteMap(self, name):
        '''Delete map with given name from database'''
    def loadMap(self, name):
        '''Load map stored in database, replace current map'''