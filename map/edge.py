from math import sqrt

class Edge(object):
    def __init(self, start_node, end_node):
        self.start = start_node
        self.end = end_node
        self.weight = self.length()
    
    def length(self):
        '''
        Return euclidian length of the edge
        '''
        return sqrt((self.end.x - self.start.x)**2 + (self.end.y - self.start.y)**2)