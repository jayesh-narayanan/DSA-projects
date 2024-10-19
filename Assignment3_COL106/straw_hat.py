'''
    This file contains the class definition for the StrawHat class.
'''
from crewmate import CrewMate
from heap import Heap,Heap_crew,comp_crew,comp_treasure


class StrawHatTreasury:
    '''
    Class to implement the StrawHat Crew Treasury
    '''

    def __init__(self, m):
        '''
        Arguments:
            m : int : Number of Crew Mates (positive integer)
        Returns:
            None
        Description:
            Initializes the StrawHat
        Time Complexity:
            O(m)
        '''

        # Write your code here
        self.crewmates=Heap_crew(comp_crew)
        self.total_number_of_treasures=0
        for i in range(m):
            self.crewmates.insert(CrewMate())

    def add_treasure(self, treasure):
        '''
        Arguments:
            treasure : Treasure : The treasure to be added to the treasury
        Returns:
            None
        Description:
            Adds the treasure to the treasury
        Time Complexity:
            O(log(m) + log(n)) where
                m : Number of Crew Mates
                n : Number of Treasures
        '''

        
        treasure.add_last_processed_time()
        treasure.is_in_heap()
        treasure.initialize_remaining_size()
        least_load_crewmate = self.crewmates.extract()
        least_load_crewmate.sum_of_sizes+=treasure.size
        least_load_crewmate.number_of_treasures+=1
        treasure.is_in_heap=True
        self.total_number_of_treasures+=1
        least_load_crewmate.treasure_arrival_time.insert(treasure)
        self.crewmates.insert(least_load_crewmate)
        
                

    

    def get_completion_time(self):
        completed_treasures = []  # List to store the completed treasures
        number_of_treasures_processed=0
        # Iterate over each crewmate independently
        for crewmate in self.crewmates.heap:
            if number_of_treasures_processed<self.total_number_of_treasures:  
                current_time = 0  # Reset current_time for each crewmate
                local_completed_treasures = []  # Store treasures processed by this crewmate
                ready_treasures = Heap(comp_treasure)  # Secondary heap for treasures ready to be processed
                is_first_treasure = True  # To track the first treasure processing

                # Process treasures based on their arrival time and priority
                while crewmate.treasure_arrival_time.heap or ready_treasures.heap:  # While there are treasures to process
                    # Handle the first treasure based on arrival time
                    if is_first_treasure and crewmate.treasure_arrival_time.heap:
                        first_treasure = crewmate.treasure_arrival_time.extract()
                        if current_time < first_treasure.arrival_time:
                            current_time = first_treasure.arrival_time  # Move to the arrival time of the first treasure
                        # Only insert the first treasure into ready_treasures if it's not already there
                        ready_treasures.insert( first_treasure)
                        first_treasure.is_in_heap = True  # Mark it as in the heap
                        is_first_treasure = False  # Mark that the first treasure has been processed

                    # Move treasures with arrival_time <= current_time to the ready heap
                    
                    while crewmate.treasure_arrival_time.heap and crewmate.treasure_arrival_time.top().arrival_time <= current_time:
                        arriving_treasure = crewmate.treasure_arrival_time.extract()  # Extract based on arrival time
                        ready_treasures.insert( arriving_treasure)  # Insert into ready heap for processing
                        arriving_treasure.is_in_heap = True  # Mark it as in the heap

                    # Find the highest priority treasure that has already arrived
                    if ready_treasures.heap:
                        # If there are ready treasures, process the highest priority one
                        treasure = ready_treasures.extract()
                        treasure.is_in_heap = False  # Mark it as being processed
                    else:
                        if current_time<crewmate.treasure_arrival_time.top().arrival_time:
                            current_time=crewmate.treasure_arrival_time.top().arrival_time
                            treasure = None  # No treasure ready to be processed

                    # If we found a treasure that can be processed
                    if treasure:
                        # Get the next treasure arrival time if there's a future treasure
                        if crewmate.treasure_arrival_time.heap:
                            next_treasure_arrival_time = crewmate.treasure_arrival_time.top().arrival_time
                        else:
                            next_treasure_arrival_time = float('inf')

                        # Process the current treasure (interrupted or fully processed)
                        if current_time + treasure.remaining_size <= next_treasure_arrival_time:
                            # Treasure is fully processed
                            completion_time = current_time + treasure.remaining_size
                            treasure.completion_time = completion_time  # Set completion time
                            local_completed_treasures.append(treasure)  # Add to completed treasures
                            current_time = completion_time  # Move current_time forward
                            number_of_treasures_processed+=1
                        else:
                            # Treasure is interrupted
                            time_processed = next_treasure_arrival_time - current_time
                            treasure.remaining_size -= time_processed  # Update remaining size
                            current_time = next_treasure_arrival_time  # Move to the next arrival

                            # Reinsert interrupted treasure back into the ready heap if it still has remaining work
                            if treasure.remaining_size > 0 and not treasure.is_in_heap:
                                ready_treasures.insert(treasure)  # Add it back to ready treasures
                                treasure.is_in_heap = True  # Mark as inserted into the heap

                # Re-insert all treasures back into the crewmate's heap with their original size
                for treasure in local_completed_treasures:
                    treasure.remaining_size = treasure.size  # Reset remaining size to original
                    # Insert the treasure back into the main treasure heap if it has not been processed
                    if not treasure.is_in_heap:
                        crewmate.treasure_arrival_time.insert(treasure)
                # Extend the completed_treasures list with the processed treasures from this crewmate
                completed_treasures.extend(local_completed_treasures)
            else:
                break
                
        # Return all treasures sorted by their ID
        return sorted(completed_treasures, key=lambda x: x.id)



