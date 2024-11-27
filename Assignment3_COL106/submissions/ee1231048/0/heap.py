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
    def _init_(self, comparison_function, init_array):
        self.heap = []
        self.compare = comparison_function
        for value in init_array:
            self.insert(value)
    def is_empty(self):
        return len(self.heap) == 0

    def left(self, index):
        return 2 * index + 1
    def right(self, index):
        return 2 * index + 2
    
    def has_left(self, index):
        return self.left(index) < len(self.heap)
    def has_right(self, index):
        return self.right(index) < len(self.heap)

    def down_heap(self, index):
        if (2 * index + 1) < len(self.heap):
            left = 2 * index + 1
            small_child = left
            if (2 * index + 2) < len(self.heap):
                right = 2 * index + 2
                if self.compare(self.heap[right], self.heap[left]):
                    small_child = right
            if self.compare(self.heap[small_child], self.heap[index]):
                self.heap[index], self.heap[small_child] = self.heap[small_child], self.heap[index]
                self.down_heap(small_child)

    def up_heap(self, index):
        parent = (index - 1) // 2
        if index > 0 and self.compare(self.heap[index], self.heap[parent]):
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            self.up_heap(parent)
            
    def insert(self, value):
        self.heap.append(value)
        self.up_heap(len(self.heap) - 1)

    def extract(self):
        if len(self.heap) == 0:
            return None
        self.heap[0], self.heap[-1] = self.heap[-1], self.heap[0]
        item = self.heap.pop()
        self.down_heap(0)
	return item

    def top(self):
        return self.heap[0] if not self.is_empty() else None

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
