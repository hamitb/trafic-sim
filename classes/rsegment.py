class Rsegment(object):
    def __init__(self , len , nlanes , edge ):
        '''
        construct a segment with floating point length and
        number of lanes from 1 to 3. edge is the edge information
        in the Map
        '''
    
    def insert_vehicle(self, vehicle):
        '''
        insert vehicle. You are free in how you present a vehicle,
        you can implement a class for it or represent as a
        dictionary. It needs to keep track of remaining road
        segments in its path and speed/timing information (start
        time, completed length, completion time or current
        position)
        '''

    def get_info(self):
        '''
        return length, number of lanes and nodes it connects in a
        tuple.
        '''

    def get_vehicles_count(self):
        '''
        return number of vehicles in the segment
        '''

    def get_capacity(self):
        '''
        return capacity of the vehicle
        '''
        
    def full(self):
        '''
        check if capacity is reached (getNVehicles()>=getCapacity())
        '''
       
    def wait_capacity(self):
        '''
        wait for a new opening for capacity (in phase 2)
        '''

    def get_stats(self):
        '''
        return statistics about the segment, max vehicles, average
        speed (for completed vehicles), current number of
        vehicles. (for phase 2)
        '''

