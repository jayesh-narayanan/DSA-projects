from bin import Bin
from object import Object
class Node:
    def __init__(self, bin, parent=None):
        self.element=bin
        self.left=None
        self.right=None
        self.height=1
    
    
class Node_obj:
    def __init__(self, object, parent=None):
        self.element =object
        self.left=None
        self.right=None
        self.parent=parent
        self.height=1