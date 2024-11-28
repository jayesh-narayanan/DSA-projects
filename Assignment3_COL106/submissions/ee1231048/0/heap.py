def comp_crew(node1,node2,arrival_time):
  return node1.get_load_to_add_treasure(arrival_time)<node2.get_load_to_add_treasure(arrival_time)

def comp_treasure(node1,node2):
      """Define comparison based on priority and treasure ID."""
      current_time = max(node1.last_processed_time, node2.last_processed_time)
      # Compare by priority, and by id if priorities are equal
      if node1.get_priority(current_time) == node2.get_priority(current_time):
          return node1.id < node2.id
      return node1.get_priority(current_time) > node2.get_priority(current_time)

def comp_arrival_time(node1,node2):
    return node1.arrival_time<node2.arrival_time



class Heap:
    '''
    Class to implement a heap with a general comparison function
    '''

    def __init__(self, comparison_function, init_array=[]):
        '''
        Arguments:
            comparison_function : function : A function that takes in two arguments and returns a boolean value
            init_array : List[Any] : The initial array to be inserted into the heap
        Returns:
            None
        Description:
            Initializes a heap with a comparison function
        Time Complexity:
            O(n) where n is the number of elements in init_array
        '''
        self.comparison_function = comparison_function
        self.heap = init_array[:]
        self.size = len(init_array)
        self.build_heap()

    def build_heap(self):
        '''
        Converts an unsorted array into a heap.
        Time Complexity: O(n) where n is the size of the array.
        '''
        for i in range((self.size // 2) - 1, -1, -1):  # Start from the last non-leaf node
            self._heapify_down(i)

    def _heapify_up(self, index):
        '''
        Helper function to maintain heap properties after insertion
        Time Complexity: O(log(n))
        '''
        parent_index = (index - 1) // 2
        while index > 0 and self.comparison_function(self.heap[index], self.heap[parent_index]):
            self.heap[index], self.heap[parent_index] = self.heap[parent_index], self.heap[index]
            index = parent_index
            parent_index = (index - 1) // 2

    def _heapify_down(self, index):
        '''
        Helper function to maintain heap properties after extraction
        Time Complexity: O(log(n))
        '''
        while True:
            left_child_index = 2 * index + 1
            right_child_index = 2 * index + 2
            best = index

            if left_child_index < self.size and self.comparison_function(self.heap[left_child_index], self.heap[best]):
                best = left_child_index

            if right_child_index < self.size and self.comparison_function(self.heap[right_child_index], self.heap[best]):
                best = right_child_index

            if best == index:  # If no swap is needed, break
                break

            self.heap[index], self.heap[best] = self.heap[best], self.heap[index]
            index = best

    def insert(self, value):
        '''
        Arguments:
            value : Any : The value to be inserted into the heap
        Returns:
            None
        Description:
            Inserts a value into the heap
        Time Complexity:
            O(log(n)) where n is the number of elements currently in the heap
        '''
        self.heap.append(value)
        self.size += 1
        self._heapify_up(self.size - 1)

    def extract(self):
        '''
        Arguments:
            None
        Returns:
            Any : The value extracted from the top of heap
        Description:
            Extracts the value from the top of heap, i.e. removes it from heap
        Time Complexity:
            O(log(n)) where n is the number of elements currently in the heap
        '''
        if self.size == 0:
            raise IndexError("Extracting from an empty heap")
        top_value = self.heap[0]
        self.heap[0] = self.heap[-1]
        self.heap.pop()
        self.size -= 1
        if self.size > 0:
            self._heapify_down(0)
        return top_value

    def top(self):
        '''
        Arguments:
            None
        Returns:
            Any : The value at the top of heap
        Description:
            Returns the value at the top of heap
        Time Complexity:
            O(1)
        '''
        if self.size == 0:
            raise IndexError("The heap is empty")
        return self.heap[0]

    def __len__(self):
        '''
        Returns:
            int : The number of elements in the heap
        '''
        return self.size

class Heap_crew:
  '''
  Class to implement a heap with general comparison function
  '''

  def __init__(self, comparison_function,arrival_time=0, init_array=[]):
      '''
      Arguments:
          comparison_function : function : A function that takes in two arguments and returns a boolean value
          init_array : List[Any] : The initial array to be inserted into the heap
      Returns:
          None
      Description:
          Initializes a heap with a comparison function
      Time Complexity:
          O(n) where n is the number of elements in init_array
      '''
      self.comparison_function = comparison_function
      self.arrival_time=arrival_time
      self.heap = init_array[:]
      self.size=len(init_array)
      self.build_heap()

  def build_heap(self):
      '''
      Converts an unsorted array into a heap.
      Time Complexity: O(n) where n is the size of the array.
      '''
      for i in range(self.size):
          self._heapify_down(i)


  def _heapify_up(self, index):
      
      parent_index = (index - 1) // 2
      while index > 0 and self.comparison_function(self.heap[index], self.heap[parent_index], self.arrival_time):
          
          self.heap[index], self.heap[parent_index] = self.heap[parent_index], self.heap[index]
          index = parent_index
      

  def _heapify_down(self, index):
      '''
      Helper function to maintain heap properties after extraction
      Time Complexity: O(log(n))
      '''
      left_child_index = 2 * index + 1
      right_child_index = 2 * index + 2
      smallest = index

      if left_child_index < self.size and self.comparison_function(self.heap[left_child_index], self.heap[smallest],self.arrival_time):
          smallest = left_child_index

      if right_child_index < self.size and self.comparison_function(self.heap[right_child_index], self.heap[smallest],self.arrival_time):
          smallest = right_child_index

      if smallest != index:
          self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
          self._heapify_down(smallest)

  def insert(self, value):
      '''
      Arguments:
          value : Any : The value to be inserted into the heap
      Returns:
          None
      Description:
          Inserts a value into the heap
      Time Complexity:
          O(log(n)) where n is the number of elements currently in the heap
      '''
      self.heap.append(value)
      self.size+=1
      self._heapify_up(self.size - 1)

  def extract(self):
      '''
      Arguments:
          None
      Returns:
          Any : The value extracted from the top of heap
      Description:
          Extracts the value from the top of heap, i.e. removes it from heap
      Time Complexity:
          O(log(n)) where n is the number of elements currently in the heap
      '''
      if len(self.heap) == 0:
          raise IndexError("Extracting from an empty heap")
      top_value = self.heap[0]
      self.heap[0] = self.heap[-1]
      self.heap.pop()
      self.size-=1
      if len(self.heap) > 0:
          self._heapify_down(0)
      return top_value

  def top(self):
      '''
      Arguments:
          None
      Returns:
          Any : The value at the top of heap
      Description:
          Returns the value at the top of heap
      Time Complexity:
          O(1)
      '''
      if len(self.heap) == 0:
          raise IndexError("The heap is empty")
      return self.heap[0]
