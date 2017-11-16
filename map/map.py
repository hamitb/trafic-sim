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
        new_node = Node(id, x, y)
        nodes[i] = new_node

    def delete_node(self, id):
        ''' 
        delete the vertice with given id. All edges connecting the vertice are also deleted
        '''
        if id not in nodes:
            return
        # Unlink children:
        for child in self.children[id]:
            del self.parent[child][id]

        # Unlink parents:
        for parent in self.parents[id]:
            del self.child[parent][id]
        
        del self.children[id]
        del self.parents[id]
        del self.nodes[id]
        

    def add_road(self, id1, id2, nlanes = 1, bidir = False):
        ''' 
        add an edge from id1 to id2. Number of lanes is set for
        each edge and if bidir is True another edge in opposite
        direction is also created. 
        '''
        start_node = nodes[id1]
        end_node = nodes[id2]
        
        new_road = Edge(start_node, end_node, nlanes)

        self.childs[id1][id2] = new_road
        self.parents[id2][id1] = new_road

        if bidir:
            self.add_road(id2, id1, nlanes)
        
        
    def delete_road(self, id1, id2, bidir = False):
        ''' 
        delete the edge between id1 and id2. If bidir is True,
        the edge in opposite direction is also deleted.
        '''
        del self.children[id1][id2]
        del self.parents[id2][id1]

        if bidir:
            self.delete_road(id2, id1)

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