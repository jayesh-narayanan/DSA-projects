from hash_table import HashSet, HashMap
from prime_generator import get_next_size

class DynamicHashSet(HashSet):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)
        
    def rehash(self):
    # Save the old table and determine the new table size
        old_table = self.table
        if self.collision_type == "Chain" or self.collision_type == "Linear":
            self.params_tuple = (self.params_tuple[0], get_next_size())
            self.table = [None] * self.params_tuple[1]
        else:
            self.params_tuple = (self.params_tuple[0], self.params_tuple[1], self.params_tuple[2], get_next_size())
            self.table = [None] * self.params_tuple[3]

        # Reinsert all elements from the old table into the new one
        self.number_of_keys=0
        if self.collision_type == "Linear" or self.collision_type == "Double":
            for x in old_table:
                if x is not None and x != "AVAILABLE":
                    super().insert(x)
        else:  # Chain rehashing
            for bucket in old_table:
                if bucket is not None:
                    for x in bucket:
                        super().insert(x)

    def insert(self, key):
        # YOU DO NOT NEED TO MODIFY THIS
        super().insert(key)
        
        if self.get_load() >= 0.5:
            self.rehash()
            
    def get_load(self):
        return super().get_load()


class DynamicHashMap(HashMap):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)
    
    def rehash(self):
    # Save the old table and determine the new table size
        old_table = self.table
        if self.collision_type == "Chain" or self.collision_type == "Linear":
            self.params_tuple = (self.params_tuple[0], get_next_size())
            self.table = [None] * self.params_tuple[1]
        else:
            self.params_tuple = (self.params_tuple[0], get_next_size(), self.params_tuple[2], self.params_tuple[3])
            self.table = [None] * self.params_tuple[3]
            self.visited = [0] * self.params_tuple[3]

        # Reinsert all elements from the old table into the new one
        self.number_of_keys=0
        if self.collision_type == "Linear" or self.collision_type == "Double":
            for x in old_table:
                if x is not None and x != "AVAILABLE":
                    super().insert(x)
        else:  # Chain rehashing
            for bucket in old_table:
                if bucket is not None:
                    for x in bucket:
                        super().insert(x)
                        
    def insert(self, key):
        # YOU DO NOT NEED TO MODIFY THIS
        super().insert(key)
        
        if self.get_load() >= 0.5:
            self.rehash()

    def get_load(self):
        return super().get_load()