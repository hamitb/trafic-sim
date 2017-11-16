class Rsegment(object):
    def __init__(self , len , nlanes , edge ):
        '''
        construct a segment with floating point length and
        number of lanes from 1 to 3. edge is the edge information
        in the Map
        '''
    
    def insert_vehicle(vehicle):
        '''
        insert vehicle. You are free in how you present a vehicle,
        you can implement a class for it or represent as a
        dictionary. It needs to keep track of remaining road
        segments in its path and speed/timing information (start
        time, completed length, completion time or current
        position)
        '''

    def get_info():
        '''
        return length, number of lanes and nodes it connects in a
        tuple.
        '''

    def get_vehicles_count():
        '''
        return number of vehicles in the segment
        '''

    def get_capacity():
        '''
        return capacity of the vehicle
        '''
        
    def full():
        '''
        check if capacity is reached (getNVehicles()>=getCapacity())
        '''
       
    def wait_capacity():
        '''
        wait for a new opening for capacity (in phase 2)
        '''

    def get_stats():
        '''
        return statistics about the segment, max vehicles, average
        speed (for completed vehicles), current number of
        vehicles. (for phase 2)
        '''

