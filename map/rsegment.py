class Vehicle(object):
    '''
    Represent Vehicle over a Rsegment
    '''
    def __init__(self , Rsegment  ):
        '''
        construct a vehicle. A vehicle will have start time in Rsegment,
        completed_length through Rsegment, completion time, and current position.
        '''
        self.Rsegment=Rsegment
        self.speed = fcrowd( Rsegment.get_vehicles_count() , Rsegment.nlanes , Rsegment.len )*60 
        #60 is kspeed which is the base speed of a car in an empty road segment
        self.x , self.y = Rsegment.edge.start_node.x , Rsegment.edge.start_node.y
        self.completed_length=0
        #self.completion_time=
        #self.start_time=
        Rsegment.insert_vehicle(self)

def fcrowd(v, l , d):
    '''returns a speed factor based on how crowded road segment is
    it returns fmax for all values in [0,cmin]. fmin for all values > cmax
    all intermediate values are linearly interpolated
    '''
    fmin ,fmax = 0.05, 1.0
    cmin,cmax = 10, 100
    c = v/( l * d)
    # vehicle per unit distance in a lane
    if c <= cmin: 
        return fmax
    elif c < cmax: 
        return fmax - ( c - cmin) * ( fmax - fmin ) / ( cmax - cmin )
    else: 
        return fmin



        
class Rsegment(object):
    def __init__(self , len , nlanes , edge ):
        '''
        construct a segment with floating point length and
        number of lanes from 1 to 3. edge is the edge information
        in the Map
        '''
        self.len = len
        self.nlanes = nlanes
        self.edge = edge
        self.vehicles = []
    
    def insert_vehicle(self, vehicle):
        '''
        insert vehicle. You are free in how you present a vehicle,
        you can implement a class for it or represent as a
        dictionary. It needs to keep track of remaining road
        segments in its path and speed/timing information (start
        time, completed length, completion time or current
        position)
        '''
        self.vehicles.append(vehicle)


    def get_info(self):
        '''
        return length, number of lanes and nodes it connects in a
        tuple.
        '''
        return ( self.len , self.nlanes , ( self.edge.start_node.node_id , self.edge.end_node.node_id ) )

    def get_vehicles_count(self):
        '''
        return number of vehicles in the segment
        '''
        return len( self.vehicles )

    def get_capacity(self):
        '''
        return capacity of the vehicle
        '''
        return int( self.nlanes*150*self.len )
        
    def full(self):
        '''
        check if capacity is reached (getNVehicles()>=getCapacity())
        '''
        return  self.get_vehicles_count() >= self.get_capacity()
       
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
        total_speed=0
        completed_vehicle_cnt=0
        for vehicle in self.vehicles:
            if vehicle.x == vehicle.Rsegment.edge.end_node.x and vehicle.y == vehicle.Rsegment.edge.end_node.y:
                completed_vehicle_cnt+=1
                total_speed=vehicle.speed
        if completed_vehicle_cnt==0:
            avg_speed=None
        else:
            avg_speed=total_speed / completed_vehicle_cnt

        return ( self.get_capacity() , avg_speed , self.get_vehicles_count() )

