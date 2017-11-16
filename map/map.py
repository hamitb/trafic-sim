from node import Node
from edge import Edge

class Map(object):
    def  __init__(self):
        ''' 
        create an empty map
        '''
        self.nodes = dict()
        self.children = dict()
        self.parents = dict()
    def add_node(self, id, x, y):
        ''' 
        create a vertice at (x,y) with given id
        '''

    def delete_node(self, id):
        ''' 
        delete the vertice with given id. All edges connecting the vertice are also deleted
        '''
        
    def add_road(self, id1, id2, nlanes = 1, bidir = True):
        ''' 
        add an edge from id1 to id2. Number of lanes is set for
        each edge and if bidir is True another edge in opposite
        direction is also created. 
        '''
    def delete_road(self, id1, id2, bidir = True):
        ''' 
        delete the edge between id1 and id2. If bidir is True,
        the edge in opposite direction is also deleted.
        '''

    def get_shortest_path(self,id1,id2):
        ''' 
        The list of edges in the shortest path from id1 and id2 is
        returned as a list of tuples. (You can use Floyd-Warshall
        algorithm to calculate all shortest paths when this is
        called for the first time, then use cached value as long as
        Map is not changed) 
        '''
    def save_map(self, name):
        '''
        Save map with given name from database
        '''
    def delete_map(self, name):
        '''
        Delete map with given name from database
        '''
    def load_map(self, name):
        '''
        Load map stored in database, replace current map
        '''