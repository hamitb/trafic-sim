import threading
from .printwc import printwc

def fcrowd(v, l, d):
    '''
    returns a speed factor based on how crowded road segment is
    it returns fmax for all values in [0,cmin]. fmin for all values > cmax
    all intermediate values are linearly interpolated
    '''
    fmin, fmax = 0.05, 1.0
    cmin, cmax = 10, 100
    c = v / (l * d)
    # vehicle per unit distance in a lane
    if c <= cmin:
        return fmax
    elif c < cmax:
        return fmax - (c - cmin) * (fmax - fmin) / (cmax - cmin)
    else:
        return fmin


class Vehicle(object):
    '''
    Represent Vehicle over a Rsegment
    '''

    def __init__(self, path, vhcl_id, k_speed):
        '''
        Construct a vehicle. A vehicle will have start time in Rsegment,
        completed_length through Rsegment, completion time, and current position.
        '''
        self.vhcl_id = vhcl_id
        self.path = path
        self.clock = 0
        self.cur_segment_clock = 0
        self.segment_count = len(path)
        self.current_segment_index = 0
        self.k_speed = k_speed
        self.current_segment = path[0]
        self.x = self.current_segment.edge.start_node.x
        self.y = self.current_segment.edge.start_node.y
        self.completed_segment_length = 0
        self.cur_completed_length = 0
        self.len_to_seg_start = 0
        self.total_path_length = sum([edge.length for edge in self.path])
        self.finish_cur_segment = False
        self.finish_path = False
        self.below_zero_limit = 1e-2

        self.speed = fcrowd(self.ahead_count(), self.current_segment.nlanes,
                            self.current_segment.length) * self.k_speed
        self.avg_speed = 0
        self.cur_segment_avg = 0

        self.current_segment.insert_vehicle(self)

    def complete_segment(self):
        if self.current_segment_index < self.segment_count - 1:
            self.current_segment_index += 1
            self.current_segment = self.path[self.current_segment_index]
            self.current_segment.insert_vehicle(self)
            self.finish_cur_segment = False
            self.speed = fcrowd(self.ahead_count(), self.current_segment.nlanes,
                                self.current_segment.length) * self.k_speed
            self.cur_segment_clock = 0
            self.completed_segment_length = 0
            for segment in self.path[:self.current_segment_index]:
                self.completed_segment_length += segment.edge.length
        else:
            self.finish_path = True
            self.completed_segment_length = 0
            for segment in self.path[:self.current_segment_index]:
                self.completed_segment_length += segment.edge.length

    def move(self):
        if not self.finish_path:
            self.speed = fcrowd(self.ahead_count(), self.current_segment.nlanes,
                                self.current_segment.length) * self.k_speed

            move_vector = self.get_vector(self.speed)
            self.x += move_vector[0]
            self.y += move_vector[1]
            self.bound_position()

            self.len_to_seg_start = ((self.y - self.current_segment.edge.start_node.y) ** 2 +
                                (self.x - self.current_segment.edge.start_node.x) ** 2) ** 0.5
            self.cur_completed_length = self.completed_segment_length + self.len_to_seg_start

            self.avg_speed = self.cur_completed_length / self.clock
            self.cur_segment_avg = self.len_to_seg_start / self.cur_segment_clock

            # printwc('yellow_bg',
            #       "{}: VehicleTime: {}, Position: ({:.2f}, {:.2f}) ==> ({:.2f}, {:.2f}) ==> ({:.2f}, {:.2f}),\n"
            #       "Path: {}/{}, Length: {:.2f}/{:.2f}\n".format(
            #           self.vhcl_id, self.clock, self.current_segment.edge.start_node.x,
            #           self.current_segment.edge.start_node.y,
            #           self.x, self.y, self.current_segment.edge.end_node.x, self.current_segment.edge.end_node.y,
            #           self.current_segment_index + 1, self.segment_count, self.cur_completed_length,
            #           self.total_path_length)
            #       )

            if self.is_segment_finish():
                self.finish_cur_segment = True

    def increase_clock(self):
        self.clock += 1
        self.cur_segment_clock += 1

    def ahead_count(self):
        return self.current_segment.get_ahead_count(self)

    def bound_position(self):
        x_positive_directed = self.get_vector(self.speed)[0] > 0
        y_positive_directed = self.get_vector(self.speed)[1] > 0

        x_end = self.current_segment.edge.end_node.x
        y_end = self.current_segment.edge.end_node.y

        x_finish = abs(self.x - x_end) < self.below_zero_limit
        y_finish = abs(self.y - y_end) < self.below_zero_limit

        if x_finish:
            self.x = x_end
        elif x_positive_directed and self.x > x_end:
            self.x = x_end
        elif not x_positive_directed and self.x < x_end:
            self.x = x_end

        if y_finish:
            self.y = y_end
        elif y_positive_directed and self.y > y_end:
            self.y = y_end
        elif not y_positive_directed and self.y < y_end:
            self.y = y_end

    def is_segment_finish(self):
        x_end = self.current_segment.edge.end_node.x
        y_end = self.current_segment.edge.end_node.y

        threshold = 1e-2

        return self.x - x_end < threshold and self.y - y_end < threshold

    def get_vector(self, speed):
        x_diff = self.current_segment.edge.end_node.x - self.current_segment.edge.start_node.x
        y_diff = self.current_segment.edge.end_node.y - self.current_segment.edge.start_node.y

        vector = [x_diff, y_diff]
        vector_normalized = [i / self.current_segment.length for i in vector]
        move_vector = [i * speed for i in vector_normalized]

        return move_vector

    def get_stats(self):
        self.stats = {
            'id': self.vhcl_id,
            'clock': self.clock,
            'speed': self.speed,
            'avg_speed': self.avg_speed,
            'c_start_x': self.current_segment.edge.start_node.x,
            'c_start_y': self.current_segment.edge.start_node.y,
            'x': self.x,
            'y': self.y,
            'c_end_x': self.current_segment.edge.end_node.x,
            'c_end_y': self.current_segment.edge.end_node.y,
            'c_segment': self.current_segment_index + 1,
            's_count': self.segment_count,
            'completed_len': self.cur_completed_length,
            'total_len': self.total_path_length,
        }
        return self.stats



class Rsegment(object):
    def __init__(self, edge, sim):
        '''
        construct a segment with floating point length and
        number of lanes from 1 to 3. edge is the edge information
        in the Map
        '''
        self.sim = sim
        self.length = edge.length
        self.edge = edge
        self.rs_id = "rs_f{}_t{}".format(self.edge.start_node.node_id, self.edge.end_node.node_id)
        self.nlanes = edge.lanes_count
        self.vehicles = []
        self.avg_speeds = dict()
        self.segment_clock = threading.Event()
        self.segment_thread = threading.Thread(target=self.step_forward, name="{}_thread".format(self.rs_id))
        self.segment_thread.start()
        self.completed = False
        self.terminated = False

        self.car_enter_exist = []

        self.sim.check()

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

    def get_tick(self):
        self.segment_clock.set()

    def get_ahead_count(self, v):
        v_pos = v.len_to_seg_start
        aheads = [vhcl.vhcl_id for vhcl in self.vehicles if vhcl.len_to_seg_start > v_pos]

        return len(aheads)

    def complete_segment(self):
        self.completed = True

    def terminate_segment(self):
        self.terminated = True

    def step_forward(self):
        while self.segment_clock.wait():
            if self.completed or self.terminated:
                self.sim.check()
                self.segment_clock.clear()
                break
            for vhcl in self.vehicles:
                vhcl.increase_clock()
                if not vhcl.finish_path:
                    vhcl.move()

                    self.avg_speeds[vhcl.vhcl_id] = {'avg': vhcl.cur_segment_avg, 'active': True}

                    if vhcl.finish_cur_segment:
                        self.avg_speeds[vhcl.vhcl_id]['active'] = False
                        vhcl.complete_segment()
                        if not vhcl.finish_path:
                            self.vehicles.remove(vhcl)
            self.sim.check()
            self.segment_clock.clear()
        return

    def get_info(self):
        '''
        return length, number of lanes and nodes it connects in a
        tuple.
        '''
        return (self.length, self.nlanes, (self.edge.start_node.node_id, self.edge.end_node.node_id))

    def get_avg_speed(self):
        speeds = [s['avg'] for (v, s) in self.avg_speeds.items()]

        if speeds == []:
            return 0

        return sum(speeds)/len(speeds)

    def get_min_speed(self):
        speeds = [v.speed for v in self.vehicles]

        if speeds == []:
            return 0

        return min(speeds)

    def get_vehicles_count(self):
        '''
        return number of vehicles in the segment
        '''
        return len(self.vehicles)

    def get_capacity(self):
        '''
        return capacity of the vehicle
        '''
        return self.nlanes * 150 * self.length

    def full(self):
        '''
        check if capacity is reached (getNVehicles()>=getCapacity())
        '''
        return self.get_vehicles_count() >= self.get_capacity()

    def get_stats(self):
        '''
        return statistics about the segment, max vehicles, average
        speed (for completed vehicles), current number of
        vehicles. (for phase 2)
            '''
        stats = {
            'CarStat': [],
            'CarEnterExist': [],
            'CarStartFinish': [],
            'EdgeStat': {},
        }
        if not self.terminated:
            for v in self.vehicles:
                stats['CarStat'].append(v.get_stats())

                if v.cur_completed_length == 0 or v.finish_cur_segment:
                    stats['CarEnterExist'].append(v.get_stats())

                if v.cur_completed_length == 0 or v.finish_path:
                    stats['CarStartFinish'].append(v.get_stats())

            stats['EdgeStat']['id'] = self.rs_id
            stats['EdgeStat']['source'] = {'x': self.edge.start_node.x, 'y':self.edge.start_node.y}
            stats['EdgeStat']['destination'] = {'x': self.edge.end_node.x, 'y': self.edge.end_node.y}
            stats['EdgeStat']['capacity'] = self.get_capacity()
            stats['EdgeStat']['active_cars'] = len([v.vhcl_id for v in self.vehicles if not v.finish_path])
            stats['EdgeStat']['cur_worst_speed'] = self.get_min_speed()
            stats['EdgeStat']['avg_speed'] = self.get_avg_speed()

        self.stats = stats['EdgeStat']
        return stats

