from flight import Flight

class Planner:
    def __init__(self, flights):
        """The Planner

        Args:
            flights (List[Flight]): A list of information of all the flights (objects of class Flight)
        """
        self.flight_list=flights
        # Adjacency list
        self.outgoing_flights_from_city=[[] for _ in range(2*len(flights))]
        # Mapping the flight_no to the flight
        self.flights_by_no=[None for _ in range(len(self.flight_list))]
        
        for i in range(len(self.flight_list)):
            self.outgoing_flights_from_city[self.flight_list[i].start_city].append(self.flight_list[i])
            self.flights_by_no[self.flight_list[i].flight_no]=self.flight_list[i]
        for i in range(len(self.outgoing_flights_from_city)):
            self.outgoing_flights_from_city[i].sort(key=lambda flight: flight.departure_time)

        # Initializing the list of the arrival time of the connecting flight
        self.time=[0 for _ in range(len(self.outgoing_flights_from_city))]
        # Initializing the path
        self.path=[None for _ in range(len(self.outgoing_flights_from_city))]
        # Initalizing a list to keep track of which flight landed into the city
        self.flight_from=[None for _ in range(len(self.outgoing_flights_from_city))]
        # Initializing the cost of the path up until that city
        self.cost=[0 for _ in range(len(self.outgoing_flights_from_city))]
        # Initializing a list to keep track of whether the city has been processed or not
        self.processed=[False for _ in range(len(self.outgoing_flights_from_city))]
        # Initializing the number of flights taken up until that city
        self.number=[0 for _ in range(len(self.outgoing_flights_from_city))]


    def least_flights_ealiest_route(self, start_city, end_city, t1, t2):
        """
        Return List[Flight]: A route from start_city to end_city, which departs after t1 (>= t1) and
        arrives before t2 (<=) satisfying: 
        The route has the least number of flights, and within routes with same number of flights, 
        arrives the earliest
        """
        route = []
        for i in range(len(self.outgoing_flights_from_city)):
            self.processed[i] = False                      
            self.time[i] = float('inf')        
            self.flight_from[i] = None                     
            self.path[i] = None                          
        
        q = Queue()
        q.enQueue((start_city, None))  
        self.time[start_city] = t1 
        # Using a modification of breadth first search 
        while not q.isEmpty():
            current_city, last_flight = q.front_element()
            q.deQueue()
            for flight in self.outgoing_flights_from_city[current_city]:
                # Skip flights that don't meet time constraints
                if (last_flight is None and flight.departure_time < t1) or flight.arrival_time > t2:
                    continue
                # Enforce the minimum layover time
                if last_flight and flight.departure_time < last_flight.arrival_time + 20:
                    continue
                # If a better route to the destination city exists, skip this flight
                if flight.arrival_time >= self.time[flight.end_city]:
                    continue

                self.time[flight.end_city] = flight.arrival_time
                self.flight_from[flight.end_city] = flight
                self.path[flight.end_city] = current_city
                q.enQueue((flight.end_city, flight))

            self.processed[current_city] = True 

        # Path reconstruction
        city = end_city
        while city != start_city:
            if city is None or self.flight_from[city] is None:
                return []  # No valid route exists
            route.append(self.flight_from[city])
            city = self.path[city]

        route.reverse()
        return route

    
    def cheapest_route(self, start_city, end_city, t1, t2):
        """
        Return List[Flight]: A route from start_city to end_city, which departs after t1 (>= t1) and
        arrives before t2 (<=) satisfying: 
        The route is a cheapest route
        """
        route=[]
        # Initialize costs, number of flights, and processed status for each city
        for i in range(len(self.cost)):
            self.cost[i]=float('inf')
            self.processed[i]=False
        self.cost[start_city]=0
        min_heap=Heap([])
        min_heap.insert((0,t1-20,[],start_city))
        # Using Dijkstra's algorithm
        while min_heap.heap:
            current_cost,current_time,path,min_index=self.find_min_unprocessed_cost(min_heap) 
            if min_index==None:
                continue
            if min_index==end_city:
                current=path
                while current:
                    if current[0]==None:
                        break
                    flight=self.flights_by_no[current[0]]
                    prev=current[1]
                    if flight:
                        route.append(flight)
                    current=prev
                return route[::-1]

            for i in range(len(self.outgoing_flights_from_city[min_index])):
                flight=self.outgoing_flights_from_city[min_index][i]
                if min_index!=start_city:
                    if self.processed[flight.end_city]==False and self.cost[min_index]!=float('inf') and self.cost[flight.end_city] > current_cost+flight.fare and flight.departure_time-current_time>=20 and flight.arrival_time<=t2:
                        self.cost[flight.end_city]=current_cost+flight.fare    # Updating the total cost upto that city
     
                else:
                    if flight.departure_time>=t1 and self.cost[flight.end_city] > current_cost+flight.fare and flight.arrival_time<=t2:   
                        self.cost[flight.end_city]=current_cost+flight.fare
                        
                if flight.arrival_time<=t2 and flight.departure_time-current_time>=20:
                    min_heap.insert((current_cost+flight.fare,flight.arrival_time,[flight.flight_no,path],flight.end_city))
            self.processed[min_index]=True
        
    
    def least_flights_cheapest_route(self, start_city, end_city, t1, t2):
        """
        Return List[Flight]: A route from start_city to end_city, which departs after t1 (>= t1) and
        arrives before t2 (<= t2) satisfying: 
        The route has the least number of flights, and within routes with the same number of flights, 
        is the cheapest.
        """
        route = []
        
        # Initialize costs, number of flights, and processed status for each city
        for i in range(len(self.cost)):
            self.number[i] = float('inf')
            self.cost[i] = float('inf')
            self.processed[i] = False
        
        self.cost[start_city] = 0
        self.time[start_city] = t1-20
        self.number[start_city] = 0

        min_heap = Heap([])
        min_heap.insert((0, 0,t1-20, [], start_city)) 
        
        # Dijkstra-like approach to find the least flights and cheapest route
        while min_heap.heap:
            current_num,current_cost,current_time,path,min_index = self.find_unprocessed_least_number_cheapest_route(min_heap)
            if min_index==None:
                continue
            if min_index==end_city:
                current=path
                while current:
                    flight=self.flights_by_no[current[0]]
                    prev=current[1]
                    if flight:
                        route.append(flight)
                    current=prev
                return route[::-1]
            
            for i in range(len(self.outgoing_flights_from_city[min_index])):
                flight = self.outgoing_flights_from_city[min_index][i]
                
                # Check for intermediate cities
                if min_index != start_city:
                    is_unprocessed = not self.processed[flight.end_city]
                    has_valid_cost = self.cost[min_index] != float('inf')
                    is_shorter_path = self.number[flight.end_city] > self.number[min_index] + 1
                    is_equal_but_cheaper = (self.number[flight.end_city] == self.number[min_index] + 1 and 
                                            self.cost[flight.end_city] > self.cost[min_index] + flight.fare)
                    has_valid_departure = flight.departure_time - current_time >= 20

                    if is_unprocessed and has_valid_cost and (is_shorter_path or is_equal_but_cheaper) and has_valid_departure and flight.arrival_time<=t2:
                        self.cost[flight.end_city] = self.cost[min_index] + flight.fare
                        self.number[flight.end_city] = self.number[min_index] + 1
                
                # Check conditions for the start city
                else:
                    is_shorter_path = self.number[flight.end_city] > self.number[min_index] + 1
                    is_equal_but_cheaper = (self.number[flight.end_city] == self.number[min_index] + 1 and 
                                            self.cost[flight.end_city] > self.cost[min_index] + flight.fare)

                    if flight.departure_time >= t1 and (is_shorter_path or is_equal_but_cheaper) and flight.arrival_time<=t2:
                        self.cost[flight.end_city] = self.cost[min_index] + flight.fare
                        self.number[flight.end_city] = self.number[min_index] + 1
                if flight.arrival_time<=t2 and flight.departure_time-current_time>=20:
                    min_heap.insert((current_num+1,current_cost+flight.fare,flight.arrival_time,[flight.flight_no,path],flight.end_city))
            self.processed[min_index]=True
        return []          

    def find_min_unprocessed_cost(self, min_heap):
        while min_heap.heap:
            current_cost, current_time, path, min_index = min_heap.extract()
            return current_cost, current_time, path, min_index
        return None, None, None, None
            
    def find_unprocessed_least_number_cheapest_route(self,min_heap):
        while min_heap.heap:
            current_num,current_cost,current_time,path,min_index=min_heap.extract()
            return current_num,current_cost,current_time,path,min_index
        return None,None,None,None,None



class Heap:
  def __init__(self, init_array=[]):
      self.heap = init_array[:]
      self.size=len(init_array)
      self.build_heap()

  def build_heap(self):
      for i in range(self.size):
          self._heapify_down(i)

  def _heapify_up(self, index):
    parent_index = (index - 1) // 2
    if index > 0 and self.heap[index]< self.heap[parent_index]:
        self.heap[index], self.heap[parent_index] = self.heap[parent_index], self.heap[index]
        self._heapify_up(parent_index)

  def _heapify_down(self, index):
      left_child_index = 2 * index + 1
      right_child_index = 2 * index + 2
      smallest = index

      if left_child_index < len(self.heap) and self.heap[left_child_index]<self.heap[smallest]:
          smallest = left_child_index

      if right_child_index < len(self.heap) and self.heap[right_child_index]< self.heap[smallest]:
          smallest = right_child_index

      if smallest != index:
          self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
          self._heapify_down(smallest)

  def insert(self, value):
     
      self.heap.append(value)
      self.size+=1
      self._heapify_up(self.size - 1)

  def extract(self):
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
      if len(self.heap) == 0:
          raise IndexError("The heap is empty")
      return self.heap[0]

class Node:
    def __init__(self,data):
        self.data=data
        self.next=None
class Queue:
    def __init__(self):
        self.front=None
        self.queueSize=0
    def enQueue(self,data):
        temp=Node(data)
        if self.front is None:
            self.front=temp
            self.queueSize= self.queueSize+1
        else:
            curr=self.front
            while curr.next!=None:
                curr=curr.next
            curr.next=temp
            self.queueSize=self.queueSize+1
    def deQueue(self):
        try:
            if self.front == None:
                raise Exception("Queue is Empty")
            else:
                temp=self.front
                self.front=self.front.next
                tempdata=temp.data
                self.queueSize= self.queueSize-1
                del temp
                return tempdata
        except Exception as e:
            print(str(e))
    def isEmpty(self):
        if self.queueSize==0:
            return True
        else:
            return False
    def size(self):
        return self.queueSize
    def front_element(self):
        try:
            if self.front == None:
                raise Exception("Queue is Empty")
            else:
                return self.front.data
        except Exception as e:
            print(str(e))