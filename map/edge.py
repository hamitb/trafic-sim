from math import sqrt

class Edge(object):
    def __init(self, start_node, end_node, lanes_count):
        self.start = start_node
        self.end = end_node
        self.lanes_count = lanes_count
        self.weight = self.length()
    
    def length(self):
        '''
        Return euclidian length of the edge
        '''
        return sqrt((self.end.x - self.start.x)**2 + (self.end.y - self.start.y)**2)