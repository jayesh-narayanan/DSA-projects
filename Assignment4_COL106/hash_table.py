from prime_generator import get_next_size

class HashTable:
    def __init__(self, collision_type, params):
        '''
        Possible collision_type:
            "Chain"     : Use hashing with chaining
            "Linear"    : Use hashing with linear probing
            "Double"    : Use double hashing
        '''
        self.collision_type=collision_type
        self.params_tuple=params
        self.number_of_keys=0
        if len(self.params_tuple)==2:
            # Chain or linear probing
            self.number_of_hashfunctions=1
            self.table=self.params_tuple[1]*[None]
            self.visited=self.params_tuple[1]*[0]
        else:
            # Double hashing
            self.number_of_hashfunctions=2
            self.table=self.params_tuple[3]*[None]
            self.visited=self.params_tuple[3]*[0]
    
    def insert(self, x):
        pass

    def find(self, key):
        pass
    
    def get_empty_slot(self, key):
        pass
    
    def get_slot(self, key):
        if self.collision_type=="Double":
            return (self.get_hashcode(self.params_tuple[0],key))%self.params_tuple[3]
        else:
            return (self.get_hashcode(self.params_tuple[0],key))%self.params_tuple[1]
        
    def get_load(self):
        if self.collision_type=="Chain" or self.collision_type=="Linear":
            return self.number_of_keys/self.params_tuple[1]
        else:
            return self.number_of_keys/self.params_tuple[3]
        
    def __str__(self):
        if self.collision_type == "Double" or self.collision_type == "Linear":
            return ' | '.join(f"{element if element not in ['AVAILABLE', None] else '<EMPTY>'}" for element in self.table)

        else:  # For chaining (with buckets)
            bucket_strings = []
            for element in self.table:
                if element is None:
                    bucket_strings.append("<EMPTY>")
                else:
                    # Use join to avoid trailing ';'
                    bucket_strings.append(' ; '.join(str(key) for key in element))
            
            # Use join to avoid trailing '|'
            return ' | '.join(bucket_strings)

    def get_hashcode(self, z, key):
        hash_code = 0
        
        for power, char in enumerate(key):
            if char.islower():
                char_code = ord(char) - 97
            else:
                char_code = ord(char) - 65 + 26
            
            term = (char_code *(z**power)) 
            hash_code = (hash_code + term)  

        return hash_code
    
    def rehash(self):
        pass

    
class HashSet(HashTable):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)
    
    def insert(self, key):
        if self.find(key):
            return
        if self.collision_type=="Chain":
            slot=self.get_empty_slot(key)
            if self.table[slot] is None:
                self.table[slot]=[]
            self.table[slot].append(key)
            self.number_of_keys+=1

        else:
            slot=self.get_empty_slot(key)
            self.table[slot]=key
            self.number_of_keys+=1


    def find(self, key):
        if self.collision_type=="Linear":
            hash_code=self.get_hashcode(self.params_tuple[0],key)
            hash_value=hash_code%self.params_tuple[1]
            probed_index=0
            while probed_index<self.params_tuple[1]:
                if self.table[hash_value]==None:
                    return False  
                elif self.table[hash_value]==key:
                    return True
                else:
                    hash_value=(hash_value+1)%self.params_tuple[1]
                    probed_index+=1
            return False 
        elif self.collision_type == "Double":
            hash_code1 = self.get_hashcode(self.params_tuple[0], key)
            hash_code2 = self.get_hashcode(self.params_tuple[1], key)

            # Initial hash values based on table size
            hash_value1 = hash_code1 % self.params_tuple[3]
            hash_value2 = self.params_tuple[2] - (hash_code2 % self.params_tuple[2])
            probed_index = 0

            while probed_index < self.params_tuple[3]:
                # Check the slot at hash_value1
                if self.table[hash_value1] is None:
                    return False
                elif self.table[hash_value1] == key:
                    return True
                else:
                    # Update hash_value1 according to double hashing formula
                    hash_value1 = (hash_value1 +  hash_value2) % self.params_tuple[3]
                    probed_index += 1

            return False
        else:
            hash_code = self.get_hashcode(self.params_tuple[0], key)
            hash_value = hash_code % self.params_tuple[1]
            bucket = self.table[hash_value]
            
            if bucket is None:
                return False
            
            for stored_key in bucket:
                if stored_key == key:
                    return True
            
            return False
    def get_slot(self,key):
        return super().get_slot(key)
    
    def get_empty_slot(self, key):
        if self.collision_type=="Linear":
            hash_code=self.get_hashcode(self.params_tuple[0],key)
            hash_value=hash_code%self.params_tuple[1]
            probed_index=0
            while probed_index<=self.params_tuple[1]:
                if self.is_available(hash_value):
                    self.visited=self.params_tuple[1]*[0]
                    return hash_value
                else:
                    self.visited[hash_value]=1
                    hash_value=(hash_value+1)%self.params_tuple[1]
                    probed_index+=1
            if probed_index==self.params_tuple[1]:
                raise Exception("Table is full")
        elif self.collision_type == "Double":
            hash_code1 = self.get_hashcode(self.params_tuple[0], key)
            hash_code2 = self.get_hashcode(self.params_tuple[1], key)

            
            hash_value1 = hash_code1 % self.params_tuple[3]  
            hash_value2 = self.params_tuple[2] - (hash_code2 % self.params_tuple[2])  
            i = 0
            while i<self.params_tuple[3]:
                
                if self.is_available(hash_value1):
                    self.visited=self.params_tuple[3]*[0]
                    return hash_value1
                else:
                    self.visited[hash_value1]=1
                    hash_value1=(hash_value1+hash_value2)%self.params_tuple[3]
                    i+=1
            if i==self.params_tuple[3]:
                raise Exception("Table is full")
        else:
            hash_code=self.get_hashcode(self.params_tuple[0],key)
            hash_value=hash_code%self.params_tuple[1]
            return hash_value

    def get_load(self):
        return super().get_load()
    
    def __str__(self):
        return super().__str__()

    def is_available(self,j):
        return self.table[j]==None or self.table[j]=="AVAILABLE"
    
    def get_hashcode(self, z, key):
        return super().get_hashcode(z,key)
    
    def __iter__(self):
        return iter(self.table)
    
class HashMap(HashTable):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)
    
    def insert(self, x):
        if self.find(x[0]):
            return
        if self.collision_type=="Chain":
            slot=self.get_empty_slot(x[0])
            if self.table[slot] is None:
                self.table[slot]=[]
            if x[0] not in self.table[slot]:
                self.table[slot].append(x)
                self.number_of_keys+=1

        else:
            slot=self.get_empty_slot(x[0])
            self.table[slot]=x
            self.number_of_keys+=1
    
    def find(self, key):
        if self.collision_type=="Linear":
            hash_code=self.get_hashcode(self.params_tuple[0],key)
            hash_value=hash_code%self.params_tuple[1]
            probed_index=0
            while probed_index<self.params_tuple[1]:
                if self.table[hash_value]==None:
                    return None 
                elif self.table[hash_value][0]==key:
                    return self.table[hash_value][1]
                else:
                    hash_value=(hash_value+1)%self.params_tuple[1]
                    probed_index+=1
            return None
        elif self.collision_type=="Double":
            hash_code1=self.get_hashcode(self.params_tuple[0],key)
            hash_code2=self.get_hashcode(self.params_tuple[1],key)
            hash_value1=hash_code1%self.params_tuple[3]
            hash_value2=self.params_tuple[2]-(hash_code2%self.params_tuple[2])
            probed_index=0
            while probed_index<self.params_tuple[3]:
                if self.table[hash_value1]==None:
                    return None  
                elif self.table[hash_value1][0]==key:
                    return self.table[hash_value1][1]
                else:
                    hash_value1=(hash_value1+hash_value2)%self.params_tuple[3]
                    probed_index+=1
            return None
        else:
            hash_code = self.get_hashcode(self.params_tuple[0], key)
            hash_value = hash_code % self.params_tuple[1]
            bucket = self.table[hash_value]
            if bucket is None:
                return None
            for stored_key in bucket:
                if stored_key[0] == key:
                    return stored_key[1]
            return None
    def get_slot(self,key):
        return super().get_slot(key)
    
    def get_empty_slot(self, key):
        if self.collision_type=="Linear":
            hash_code=self.get_hashcode(self.params_tuple[0],key)
            hash_value=hash_code%self.params_tuple[1]
            probed_index=0
            while probed_index<self.params_tuple[1]:
                if self.is_available(hash_value):
                    self.visited=self.params_tuple[1]*[0]
                    return hash_value
                else:
                    self.visited[hash_value]=1
                    hash_value=(hash_value+1)%self.params_tuple[1]
                    probed_index+=1
            if probed_index==self.params_tuple[1]:
                raise Exception("Table is full")
                
        elif self.collision_type=="Double":
            hash_code1=self.get_hashcode(self.params_tuple[0],key)
            hash_code2=self.get_hashcode(self.params_tuple[1],key)
            hash_value1=hash_code1%self.params_tuple[3]
            hash_value2=self.params_tuple[2]-(hash_code2%self.params_tuple[2])
            probed_index=0
            while probed_index<self.params_tuple[3]:
                if self.is_available(hash_value1):
                    self.visited=self.params_tuple[3]*[0]
                    return hash_value1
                else:
                    self.visited[hash_value1]=1
                    hash_value1=(hash_value1+hash_value2)%self.params_tuple[3]
                    probed_index+=1
            if probed_index==self.params_tuple[3]:
                raise Exception("Table is full")
        else:
            hash_code=self.get_hashcode(self.params_tuple[0],key)
            hash_value=hash_code%self.params_tuple[1]
            return hash_value
    
    def get_load(self):
        super().get_load()
    
    def __str__(self):
        super().__str__()

    def is_available(self,j):
        return self.table[j]==None or self.table[j]=="AVAILABLE"
    
    def get_hashcode(self, z, key):
        return super().get_hashcode(z,key)