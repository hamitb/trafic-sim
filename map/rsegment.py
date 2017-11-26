import threading

class Vehicle(object):
    '''
    Represent Vehicle over a Rsegment
    '''
    def __init__(self, path):
        '''
        Construct a vehicle. A vehicle will have start time in Rsegment,
        completed_length through Rsegment, completion time, and current position.
        '''
        self.path=path
        self.segment_count = len(path)
        self.current_segment_index = 0
        self.current_segment = path[0]
        self.speed = fcrowd(self.current_segment.get_vehicles_count(), self.current_segment.nlanes, self.current_segment.length)*60 
        self.x = self.current_segment.edge.start_node.x
        self.y = self.current_segment.edge.start_node.y
        self.completed_length=0
        self.vector = []
        self.finish_path = False
        
        self.vhcl_tick = threading.Event()
        self.move_thread = threading.Thread(target=self.move)
        self.move_thread.start()
        self.current_segment.insert_vehicle(self)
    
    def complete_segment(self):
        if self.current_segment_index < self.segment_count-1:
            self.current_segment_index += 1
            self.current_segment = self.path[self.current_segment_index]
            self.current_segment.insert_vehicle(self)
            completed_length = 0
            for segment in self.path[:self.current_segment_index]:
                completed_length += segment.edge.length
        else:
            self.finish_path = True
            completed_length = 0
            for segment in self.path[:self.current_segment_index]:
                completed_length += segment.edge.length
        
    def move(self):
        while not self.finish_path and self.vhcl_tick.wait():
            move_vector = self.get_vector(self.speed)
            self.x += move_vector[0]
            self.y += move_vector[1]

    def get_vector(self, speed):
        x_diff = self.current_segment.edge.end_node.x - self.current_segment.edge.start_node.x
        y_diff = self.current_segment.edge.end_node.y - self.current_segment.edge.start_node.y

        vector = [x_diff, y_diff]
        vector_normalized = [i/self.current_segment.length for i in vector]
        move_vector = [i * speed for i in vector_normalized]

        return move_vector




def fcrowd(v, l , d):
    '''
    returns a speed factor based on how crowded road segment is
    it returns fmax for all values in [0,cmin]. fmin for all values > cmax
    all intermediate values are linearly interpolated
    '''
    fmin, fmax = 0.05, 1.0
    cmin, cmax = 10, 100
    c = v / (l*d)
    # vehicle per unit distance in a lane
    if c <= cmin: 
        return fmax
    elif c < cmax: 
        return fmax - ( c - cmin) * ( fmax - fmin ) / ( cmax - cmin )
    else: 
        return fmin



        
class Rsegment(object):
    def __init__(self , nlanes , edge):
        '''
        construct a segment with floating point length and
        number of lanes from 1 to 3. edge is the edge information
        in the Map
        '''
        self.length = edge.length
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
        return (self.length, self.nlanes,(self.edge.start_node.node_id, self.edge.end_node.node_id))

    def get_vehicles_count(self):
        '''
        return number of vehicles in the segment
        '''
        return len(self.vehicles)

    def get_capacity(self):
        '''
        return capacity of the vehicle
        '''
        return int(self.nlanes*150*self.length)
        
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

        return (self.get_capacity() , avg_speed , self.get_vehicles_count())

