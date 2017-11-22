from models import *
from math import sqrt

class Node(object):
    def __init__(self, node_id, x, y):
        self.x = x
        self.y = y
        self.node_id = node_id

class Edge(object):
    def __init__(self, start_node, end_node, lanes_count):
        self.start_node = start_node
        self.end_node = end_node
        self.lanes_count = lanes_count
        self.length = self.get_length()
    def get_length(self):
        '''
        Return euclidian length of the edge
        '''
        squared_sum = (self.end_node.x - self.start_node.x)**2 + (self.end_node.y - self.start_node.y)**2
        root_ss = sqrt(squared_sum)
        rounded_length = round(root_ss, 4)
        
        return rounded_length

class Map(object):
    def  __init__(self):
        '''
        create an empty map
        '''
        self.nodes = dict()
        self.children = dict()
        self.parents = dict()
        self.name = ''
    def add_node(self, node_id, x, y):
        '''
        create a vertice at (x,y) with given id
        '''
        new_node = Node(node_id, x, y)
        self.nodes[node_id] = new_node
        self.children[node_id] = dict()
        self.parents[node_id] = dict()

    def delete_node(self, node_id):
        '''
        delete the vertice with given id. All edges connecting the vertice are also deleted
        '''
        if node_id not in self.nodes:
            return
        # Unlink children:
        for child in self.children[node_id]:
            del self.parents[child][node_id]

        # Unlink parents:
        for parent in self.parents[node_id]:
            del self.children[parent][node_id]
        
        del self.children[node_id]
        del self.parents[node_id]
        del self.nodes[node_id]
 
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

    def get_shortest_path(self, id1, id2, path=[]):
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
                        len_newpath=len_newpath+edge.length
                    if shortest_path!=None:
                        len_shortest=0
                        for edge2 in new_path:
                            len_shortest=len_shortest+edge2.length
                        if len_newpath<len_shortest :
                            shortest_path=new_path
        return shortest_path

    def get_raw_nodes(self):
        raw_data = [{'node_id': node_id, 'x': node.x, 'y': node.y, 'map_name': self.name} \
                            for node_id, node in self.nodes.items()]

        return raw_data

    def get_raw_edges(self):
        raw_edges = []

        for start_node in self.children:
            for end_node, edge_between in self.children[start_node].items():
                raw_edges.append({
                    'start_node': edge_between.start_node.node_id,
                    'end_node': edge_between.end_node.node_id,
                    'lanes_count': edge_between.lanes_count,
                    'length': edge_between.length,
                    'map_name': self.name,
                })

        return raw_edges

    def save_map(self, name):
        '''
        Save map with given name from database
        '''
        self.name = name
        MapModel.insert(name=name).execute()

        raw_nodes = self.get_raw_nodes()
        raw_edges = self.get_raw_edges()

        with db.atomic():
            NodeModel.insert_many(raw_nodes).execute()
            EdgeModel.insert_many(raw_edges).execute()

    def delete_map(self, name):
        '''
        Delete map with given name from database
        '''
    def load_map(self, name):
        '''
        Load map stored in database, replace current map
        '''