"""
Created on Aug 9, 2015

@author: ldhuy
"""

class Node(object):
    """
    Node for pathMap and deMap
    """


    def __init__(self, path, neighbors, typ):
        """
        Constructor
        """
        self._path = []
        self._neighbors = set()
        self._type = ''
        self.path = path
        self.neighbors = neighbors
        self.type = typ
        
    @property
    def path(self):
        return self._path
    
    @path.setter
    def path(self, path):
        self._path = path
        
    @property
    def neighbors(self):
        return self._neighbors
    
    @neighbors.setter
    def neighbors(self, neighbors):
        self._neighbors = neighbors
    
    @property
    def type(self):
        return self._type
    
    @type.setter
    def type(self, typ):
        self._type = typ
    
    def add_neighbor(self, neighbor):
        self._neighbors.add(neighbor)
        
    def __str__(self, *args, **kwargs):
#         s = "Path: {0}\nNumber of neighbors: {1}".format(str(self.path), str(len(self.neighbors)))
        s = str(self.path)
        return s
    
    def __repr__(self, *args, **kwargs):
#         s = "Path: {0}\nNumber of neighbors: {1}".format(str(self.path), str(len(self.neighbors)))
        s = str(self.path)
        return s
        