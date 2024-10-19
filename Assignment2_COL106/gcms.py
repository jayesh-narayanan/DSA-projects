from bin import Bin
from avl import AVLTree, comp_4
from avl import comp_1, comp_2, comp_3
from object import Object, Color
from exceptions import NoBinFoundException
from node import Node, Node_obj

class GCMS:
    def __init__(self):
     # Maintain all the Bins and Objects in GCMS
        self.AVLTree_capacity_greater_bin_id=AVLTree(comp_1)
        self.AVLTree_bin_id=AVLTree(comp_2)
        self.AVLTree_object=AVLTree(comp_3)
        self.AVLTree_capacity_lesser_bin_id=AVLTree(comp_4)

    def add_bin(self, bin_id, capacity):
        # Insert into AVLTree_capacity using the provided insert method
        b = Bin(bin_id, capacity)
        new_node_greater = Node(b)
        self.AVLTree_capacity_greater_bin_id.root = self.AVLTree_capacity_greater_bin_id.insert_into_capacity_tree_greater_bin_id(self.AVLTree_capacity_greater_bin_id.root, new_node_greater)
        new_node_lesser=Node(b)
        self.AVLTree_capacity_lesser_bin_id.root = self.AVLTree_capacity_greater_bin_id.insert_into_capacity_tree_lesser_bin_id(self.AVLTree_capacity_lesser_bin_id.root, new_node_lesser)
        new_node_bin=Node(b)
        # Insert into AVLTree_bin_id manually
        self.AVLTree_bin_id.root = self.AVLTree_bin_id.insert_into_bin_id_tree(self.AVLTree_bin_id.root, new_node_bin)

    def bin_info(self, bin_id):
        current = self.AVLTree_bin_id.root
    
        while current is not None:
    
            if bin_id == current.element.bin_id:
                return (current.element.capacity,current.element.objects)
    
            if bin_id < current.element.bin_id:
                current = current.left
            else:
                current = current.right
    
    def object_info(self, object_id):
     # returns the bin_id in which the object is stored
        current = self.AVLTree_object.root
    
        while current is not None:
            if object_id == current.element.object_id:
                return current.element.bin_stored.bin_id
            if object_id < current.element.object_id:
                current = current.left
            else:
                current = current.right
    def add_object(self, object_id, size, color):
        # Determine the best bin based on color rules
        best_bin = None
        if color == Color.BLUE:
            # Compact Fit, Least ID
            best_bin = self.find_best_bin(size, smallest_capacity=True, least_id=True)
        elif color == Color.YELLOW:
            # Compact Fit, Greatest ID
            best_bin = self.find_best_bin(size, smallest_capacity=True, least_id=False)
        elif color == Color.RED:
            # Largest Fit, Least ID
            best_bin = self.find_best_bin(size, smallest_capacity=False, least_id=True)
        elif color == Color.GREEN:
            # Largest Fit, Greatest ID
            best_bin = self.find_best_bin(size, smallest_capacity=False, least_id=False)

        # If no bin is found, raise an exception
        if best_bin is None:
            raise NoBinFoundException()
        o=Object(object_id,size,color)
        new_node=Node_obj(o)
        new_bin_greater=Node(best_bin.element)
        new_bin_lesser=Node(best_bin.element)
        self.AVLTree_capacity_greater_bin_id.root=self.AVLTree_capacity_greater_bin_id.delete_from_capacity_tree_greater_bin_id(self.AVLTree_capacity_greater_bin_id.root, best_bin.element)
        self.AVLTree_capacity_lesser_bin_id.root=self.AVLTree_capacity_lesser_bin_id.delete_from_capacity_tree_lesser_bin_id(self.AVLTree_capacity_lesser_bin_id.root, best_bin.element)
        new_bin_greater.element.capacity-=size
        new_bin_greater.element.add_object(o)
        o.bin_stored=new_bin_greater.element
        self.AVLTree_capacity_greater_bin_id.root = self.AVLTree_capacity_greater_bin_id.insert_into_capacity_tree_greater_bin_id(self.AVLTree_capacity_greater_bin_id.root, new_bin_greater)
        self.AVLTree_capacity_lesser_bin_id.root = self.AVLTree_capacity_lesser_bin_id.insert_into_capacity_tree_lesser_bin_id(self.AVLTree_capacity_lesser_bin_id.root, new_bin_lesser)
        self.AVLTree_object.root = self.AVLTree_object.insert_into_object_id_tree(self.AVLTree_object.root, new_node)




    def find_best_bin(self, size, smallest_capacity, least_id):
        if (smallest_capacity and not least_id) or (not smallest_capacity and least_id):
            # Red or Yellow objects
            current = self.AVLTree_capacity_lesser_bin_id.root
            best_bin=None
            while current is not None:
                if current.element.capacity >= size:
                    if best_bin is None:
                        best_bin = current
                    else:
                        if smallest_capacity:
                            if current.element.capacity < best_bin.element.capacity:
                                best_bin = current
                            elif current.element.capacity == best_bin.element.capacity and current.element.bin_id>best_bin.element.bin_id:
                                best_bin=current
                            current=current.left
                                
                                
                        else:
                            if current.element.capacity > best_bin.element.capacity:
                                best_bin = current
                            elif current.element.capacity == best_bin.element.capacity and current.element.bin_id<best_bin.element.bin_id:
                                best_bin=current
                            current=current.right


                else:
                    current=current.right
                    
        else:
            # Green or Blue objects
            current = self.AVLTree_capacity_greater_bin_id.root
            best_bin=None
            while current is not None:
                if current.element.capacity >= size:
                    if best_bin is None:
                        best_bin = current
                    else:
                        if smallest_capacity:
                            if current.element.capacity < best_bin.element.capacity:
                                best_bin = current
                            elif current.element.capacity == best_bin.element.capacity and current.element.bin_id<best_bin.element.bin_id:
                                best_bin=current
                            current=current.left

                        else:
                            if current.element.capacity > best_bin.element.capacity:
                                best_bin = current
                            elif current.element.capacity == best_bin.element.capacity and current.element.bin_id>best_bin.element.bin_id:
                                best_bin=current
                            current=current.right


                else:
                    current=current.right
                            
        return best_bin

    def delete_object(self, object_id):
        node_obj=self.AVLTree_object.search_in_object_id_tree(self.AVLTree_object.root, object_id)
        size=node_obj.element.size
        bin_stored=node_obj.element.bin_stored
        new_bin_greater=Node(bin_stored)
        new_bin_lesser=Node(bin_stored)
        self.AVLTree_object.root=self.AVLTree_object.delete_from_object_id_tree(self.AVLTree_object.root, object_id)
        self.AVLTree_capacity_greater_bin_id.root=self.AVLTree_capacity_greater_bin_id.delete_from_capacity_tree_greater_bin_id(self.AVLTree_capacity_greater_bin_id.root, bin_stored)
        self.AVLTree_capacity_lesser_bin_id.root=self.AVLTree_capacity_lesser_bin_id.delete_from_capacity_tree_lesser_bin_id(self.AVLTree_capacity_lesser_bin_id.root, bin_stored)
        bin_stored.capacity+=size
        bin_stored.remove_object(object_id)
        self.AVLTree_capacity_greater_bin_id.root = self.AVLTree_capacity_greater_bin_id.insert_into_capacity_tree_greater_bin_id(self.AVLTree_capacity_greater_bin_id.root, new_bin_greater)
        self.AVLTree_capacity_lesser_bin_id.root = self.AVLTree_capacity_lesser_bin_id.insert_into_capacity_tree_lesser_bin_id(self.AVLTree_capacity_lesser_bin_id.root, new_bin_lesser)
        
        