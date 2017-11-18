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
        
        self.nodes[id] = new_node
        self.children[id] = dict()
        self.parents[id] = dict()

    def delete_node(self, id):
        ''' 
        delete the vertice with given id. All edges connecting the vertice are also deleted
        '''
        if id not in self.nodes:
            return
        # Unlink children:
        for child in self.children[id]:
            del self.parents[child][id]

        # Unlink parents:
        for parent in self.parents[id]:
            del self.children[parent][id]
        
        del self.children[id]
        del self.parents[id]
        del self.nodes[id]
        

    def add_road(self, id1, id2, nlanes = 1, bidir = False):
        ''' 
        add an edge from id1 to id2. Number of lanes is set for
        each edge and if bidir is True another edge in opposite
        direction is also created. 
        '''
        start_node = self.nodes[id1]
        end_node = self.nodes[id2]
        
        new_road = Edge(start_node, end_node, nlanes)

        self.children[id1][id2] = new_road
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

    def get_shortest_path(self,id1,id2,path=[]):
        ''' 
        The list of edges in the shortest path from id1 and id2 is
        returned as a list of tuples. (You can use Floyd-Warshall
        algorithm to calculate all shortest paths when this is
        called for the first time, then use cached value as long as
        Map is not changed) 
        '''
        

        if id1==id2:
            return path
        if id1 not in self.nodes:
            return None
        shortest_path =None
        

        for child in self.children[id1]:
            path= path + [ self.children[id1][child] ] 
            if child not in path:
                new_path=self.get_shortest_path(child,id2,path)
                if new_path !=None :
                    len_newpath=0
                    for edge in new_path:
                        len_newpath=len_newpath+edge.length()
                    if shortest_path!=None:
                        len_shortest=0
                        for edge2 in new_path:
                            len_shortest=len_shortest+edge2.length()
                        if len_newpath<len_shortest :
                            shortest_path=new_path
        return shortest_path


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