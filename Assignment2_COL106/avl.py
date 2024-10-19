from bin import Bin
from node import Node,Node_obj

def comp_1(node_1, node_2):
    if (node_1.element.capacity>node_2.element.capacity):
        return True
    elif (node_1.element.capacity<node_2.element.capacity):
        return False
    else:
        return node_1.element.bin_id>node_2.element.bin_id

def comp_2(node_1,node_2):
    return node_1.element.bin_id >node_2.element.bin_id

def comp_3(node_1, node_2):
    return node_1.element.object_id>node_2.element.object_id

def comp_4(node_1, node_2):
    if (node_1.element.capacity>node_2.element.capacity):
        return True
    elif (node_1.element.capacity<node_2.element.capacity):
        return False
    else:
        return node_1.element.bin_id<node_2.element.bin_id
    
    
class AVLTree:
    def __init__(self,compare_function):
        self.root = None
        self.comparator=compare_function

    def height(self, node):
        if not node:
            return 0
        return node.height

    def balance(self, node):
        if not node:
            return 0
        return self.height(node.left) - self.height(node.right)

    def insert_into_capacity_tree_greater_bin_id(self, root, node):
        if not root:
            return node  # Create a node with the Bin object
        elif node.element.capacity < root.element.capacity or (node.element.capacity == root.element.capacity and node.element.bin_id < root.element.bin_id):
            root.left = self.insert_into_capacity_tree_greater_bin_id(root.left, node)
        else:
            root.right = self.insert_into_capacity_tree_greater_bin_id(root.right, node)

        root.height = 1 + max(self.height(root.left), self.height(root.right))
        balance = self.balance(root)

        # Left rotation (Case 1: Left Left)
        if balance > 1 and (node.element.capacity < root.left.element.capacity or (node.element.capacity == root.left.element.capacity and node.element.bin_id < root.left.element.bin_id)):
            return self.right_rotate(root)

        # Right rotation (Case 2: Right Right)
        if balance < -1 and (node.element.capacity > root.right.element.capacity or (node.element.capacity == root.right.element.capacity and node.element.bin_id > root.right.element.bin_id)):
            return self.left_rotate(root)

        # Left-Right rotation (Case 3: Left Right)
        if balance > 1 and (node.element.capacity > root.left.element.capacity or (node.element.capacity == root.left.element.capacity and node.element.bin_id > root.left.element.bin_id)):
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # Right-Left rotation (Case 4: Right Left)
        if balance < -1 and (node.element.capacity < root.right.element.capacity or (node.element.capacity == root.right.element.capacity and node.element.bin_id < root.right.element.bin_id)):
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def insert_into_capacity_tree_lesser_bin_id(self, root, node):
        if not root:
            return node  # Create a node with the Bin object
        elif node.element.capacity < root.element.capacity or (node.element.capacity == root.element.capacity and node.element.bin_id > root.element.bin_id):
            root.left = self.insert_into_capacity_tree_greater_bin_id(root.left, node)
        else:
            root.right = self.insert_into_capacity_tree_greater_bin_id(root.right, node)

        root.height = 1 + max(self.height(root.left), self.height(root.right))
        balance = self.balance(root)

        # Left rotation (Case 1: Left Left)
        if balance > 1 and (node.element.capacity < root.left.element.capacity or (node.element.capacity == root.left.element.capacity and node.element.bin_id > root.left.element.bin_id)):
            return self.right_rotate(root)

        # Right rotation (Case 2: Right Right)
        if balance < -1 and (node.element.capacity > root.right.element.capacity or (node.element.capacity == root.right.element.capacity and node.element.bin_id < root.right.element.bin_id)):
            return self.left_rotate(root)

        # Left-Right rotation (Case 3: Left Right)
        if balance > 1 and (node.element.capacity > root.left.element.capacity or (node.element.capacity == root.left.element.capacity and node.element.bin_id < root.left.element.bin_id)):
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # Right-Left rotation (Case 4: Right Left)
        if balance < -1 and (node.element.capacity < root.right.element.capacity or (node.element.capacity == root.right.element.capacity and node.element.bin_id > root.right.element.bin_id)):
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def delete_from_capacity_tree_greater_bin_id(self, root, bin):
        if not root:
            return root

        # Traverse the tree to find the node to delete
        if bin.capacity < root.element.capacity or (bin.capacity == root.element.capacity and bin.bin_id < root.element.bin_id):
            root.left = self.delete_from_capacity_tree_greater_bin_id(root.left, bin)
        elif bin.capacity > root.element.capacity or (bin.capacity == root.element.capacity and bin.bin_id > root.element.bin_id):
            root.right = self.delete_from_capacity_tree_greater_bin_id(root.right, bin)
        else:
            # Node found
            if not root.left:  # Case 1: Node has no left child
                temp = root.right
                root = None
                return temp
            elif not root.right:  # Case 2: Node has no right child
                temp = root.left
                root = None
                return temp

            # Case 3: Node has two children, replace with in-order successor
            temp = self.min_value_node(root.right)  # In-order successor (smallest in the right subtree)
            root.element = temp.element  # Replace root's value with the successor's value
            root.right = self.delete_from_capacity_tree_greater_bin_id(root.right, temp.element)  # Delete the in-order successor

        # Update the height of the current node
        root.height = 1 + max(self.height(root.left), self.height(root.right))

        # Get the balance factor of the current node to check if it's balanced
        balance = self.balance(root)

        # Perform rotations if the node becomes unbalanced
        # Left rotation
        if balance > 1 and self.balance(root.left) >= 0:
            return self.right_rotate(root)

        # Right rotation
        if balance < -1 and self.balance(root.right) <= 0:
            return self.left_rotate(root)

        # Left-Right rotation
        if balance > 1 and self.balance(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # Right-Left rotation
        if balance < -1 and self.balance(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def delete_from_capacity_tree_lesser_bin_id(self, root, bin):
        if not root:
            return root

        # Traverse the tree to find the node to delete
        if bin.capacity < root.element.capacity or (bin.capacity == root.element.capacity and bin.bin_id > root.element.bin_id):
            root.left = self.delete_from_capacity_tree_greater_bin_id(root.left, bin)
        elif bin.capacity > root.element.capacity or (bin.capacity == root.element.capacity and bin.bin_id < root.element.bin_id):
            root.right = self.delete_from_capacity_tree_greater_bin_id(root.right, bin)
        else:
            # Node found
            if not root.left:  # Case 1: Node has no left child
                temp = root.right
                root = None
                return temp
            elif not root.right:  # Case 2: Node has no right child
                temp = root.left
                root = None
                return temp

            # Case 3: Node has two children, replace with in-order successor
            temp = self.min_value_node(root.right)  # In-order successor (smallest in the right subtree)
            root.element = temp.element  # Replace root's value with the successor's value
            root.right = self.delete_from_capacity_tree_greater_bin_id(root.right, temp.element)  # Delete the in-order successor

        # Update the height of the current node
        root.height = 1 + max(self.height(root.left), self.height(root.right))

        # Get the balance factor of the current node to check if it's balanced
        balance = self.balance(root)

        # Perform rotations if the node becomes unbalanced
        # Left rotation
        if balance > 1 and self.balance(root.left) >= 0:
            return self.right_rotate(root)

        # Right rotation
        if balance < -1 and self.balance(root.right) <= 0:
            return self.left_rotate(root)

        # Left-Right rotation
        if balance > 1 and self.balance(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # Right-Left rotation
        if balance < -1 and self.balance(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root


    def left_rotate(self, z):
        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        z.height = 1 + max(self.height(z.left), self.height(z.right))
        y.height = 1 + max(self.height(y.left), self.height(y.right))

        return y

    def right_rotate(self, z):
        y = z.left
        T3 = y.right

        y.right = z
        z.left = T3

        z.height = 1 + max(self.height(z.left), self.height(z.right))
        y.height = 1 + max(self.height(y.left), self.height(y.right))

        return y

    def min_value_node(self, root):
        current = root
        while current.left:
            current = current.left
        return current

    

    def insert_into_bin_id_tree(self, root, new_node):
        if root is None:
            return new_node
        elif new_node.element.bin_id < root.element.bin_id:
            root.left = self.insert_into_bin_id_tree(root.left, new_node)
        else:
            root.right = self.insert_into_bin_id_tree(root.right, new_node)

        # Update height and balance the tree
        root.height = 1 + max(self.height(root.left), self.height(root.right))
        balance_factor = self.balance(root)

        # Left Left Case
        if balance_factor > 1 and new_node.element.bin_id < root.left.element.bin_id:
            return self.right_rotate(root)

        # Right Right Case
        if balance_factor < -1 and new_node.element.bin_id > root.right.element.bin_id:
            return self.left_rotate(root)

        # Left Right Case
        if balance_factor > 1 and new_node.element.bin_id > root.left.element.bin_id:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # Right Left Case
        if balance_factor < -1 and new_node.element.bin_id < root.right.element.bin_id:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def insert_into_object_id_tree(self, root, new_node):
        if root is None:
            return new_node
        elif new_node.element.object_id < root.element.object_id:
            root.left = self.insert_into_object_id_tree(root.left, new_node)
        else:
            root.right = self.insert_into_object_id_tree(root.right, new_node)

        # Update height and balance the tree
        root.height = 1 + max(self.height(root.left), self.height(root.right))
        balance_factor = self.balance(root)

        # Left Left Case
        if balance_factor > 1 and new_node.element.object_id < root.left.element.object_id:
            return self.right_rotate(root)

        # Right Right Case
        if balance_factor < -1 and new_node.element.object_id > root.right.element.object_id:
            return self.left_rotate(root)

        # Left Right Case
        if balance_factor > 1 and new_node.element.object_id > root.left.element.object_id:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # Right Left Case
        if balance_factor < -1 and new_node.element.object_id < root.right.element.object_id:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def search_in_object_id_tree(self, root, object_id):
        if root is None or root.element.object_id == object_id:
            return root
        elif root.element.object_id < object_id:
            return self.search_in_object_id_tree(root.right, object_id)
        else:
            return self.search_in_object_id_tree(root.left, object_id)

    def delete_from_object_id_tree(self, root, object_id):
        if not root:
            return root

        # Traverse the tree to find the node to delete
        if object_id < root.element.object_id :
            root.left = self.delete_from_object_id_tree(root.left, object_id)
        elif object_id > root.element.object_id:
            root.right = self.delete_from_object_id_tree(root.right, object_id)
        else:
            # Node found
            if not root.left:  # Case 1: Node has no left child
                temp = root.right
                root = None
                return temp
            elif not root.right:  # Case 2: Node has no right child
                temp = root.left
                root = None
                return temp

            # Case 3: Node has two children, replace with in-order successor
            temp = self.min_value_node(root.right)  # In-order successor (smallest in the right subtree)
            root.element = temp.element  # Replace root's value with the successor's value
            root.right = self.delete_from_object_id_tree(root.right, temp.element.object_id)  # Delete the in-order successor

        # Update the height of the current node
        root.height = 1 + max(self.height(root.left), self.height(root.right))

        # Get the balance factor of the current node to check if it's balanced
        balance = self.balance(root)

        # Perform rotations if the node becomes unbalanced
        # Left rotation
        if balance > 1 and self.balance(root.left) >= 0:
            return self.right_rotate(root)

        # Right rotation
        if balance < -1 and self.balance(root.right) <= 0:
            return self.left_rotate(root)

        # Left-Right rotation
        if balance > 1 and self.balance(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # Right-Left rotation
        if balance < -1 and self.balance(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root
        
   
