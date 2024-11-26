'''
    Python file to implement the class CrewMate
'''
from heap import Heap
from heap import comp_arrival_time
class CrewMate:
    '''
    Class to implement a crewmate
    '''

    def __init__(self):
        '''
        Arguments:
            None
        Returns:
            None
        Description:
            Initializes the crewmate
        '''

        # Write your code here
        self.load=0
        self.treasure_arrival_time=Heap(comp_arrival_time)
        self.number_of_treasures=0
        self.sum_of_sizes=0
        self.load_is_zero=0
    # Add more methods if required
    def get_load_to_add_treasure(self,t):
        if self.number_of_treasures>0:
            if (self.sum_of_sizes-t+self.load_is_zero<0):
                self.load_is_zero=t-self.sum_of_sizes
                return 0
            else:
                return self.sum_of_sizes-t+self.load_is_zero
        else:
            self.load_is_zero=t
            return 0