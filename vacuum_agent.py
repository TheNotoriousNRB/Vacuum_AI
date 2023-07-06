from une_ai.models import Agent

class VacuumAgent(Agent):

    WHEELS_DIRECTIONS = ['north', 'south', 'west', 'east']

    def __init__(self, agent_program):
        super().__init__(
            agent_name='vacuum_agent',
            agent_program=agent_program
        )

        
    # TODO: add all the sensors
    def add_all_sensors(self):
        self.add_sensor('location-sensor', (0,0), lambda v:isinstance(v, tuple) and len(v) == 2 and isinstance(v[0], int) and isinstance(v[1], int))
        self.add_sensor('battery-level', 0, lambda v:isinstance(v, int) or isinstance(v, float))
        self.add_sensor('dirt-sensor-center', False, lambda v:v in [True, False])
        self.add_sensor('dirt-sensor-north', False, lambda v:v in [True, False])
        self.add_sensor('dirt-sensor-south', False, lambda v:v in [True, False])
        self.add_sensor('dirt-sensor-east', False, lambda v:v in [True, False])
        self.add_sensor('dirt-sensor-west', False, lambda v:v in [True, False])
        self.add_sensor('bumper-sensor-north', False, lambda v:v in [True, False])
        self.add_sensor('bumper-sensor-south', False, lambda v:v in [True, False])
        self.add_sensor('bumper-sensor-east', False, lambda v:v in [True, False])
        self.add_sensor('bumper-sensor-west', False, lambda v:v in [True, False])
    
    # TODO: add all the actuators
    def add_all_actuators(self):
        self.add_actuator('wheels-direction', 'north', lambda v: v in VacuumAgent.WHEELS_DIRECTIONS)
        self.add_actuator('vacuum-power', 0, lambda v: v in [0, 1])
        self.add_actuator('suction-power', 0, lambda v: v in [0,1])

    # TODO: add all the actions
    def add_all_actions(self):
        # TODO: implement the following methods
        self.add_action('start-cleaning', lambda: {'vacuum-power': 1} if not self.is_out_of_charge() else {})
        self.add_action('stop-cleaning', lambda: {'vacuum-power': 0})
        self.add_action('activate-suction-mechanism', lambda: {'suction-power': 1} if not self.is_out_of_charge() else {})
        self.add_action('deactivate-suction-mechanism', lambda:{'suction-power': 0})
        self.add_action('change-direction-north', lambda:{'wheels-direction': 'north'})
        self.add_action('change-direction-east', lambda:{'wheels-direction': 'east'})
        self.add_action('change-direction-west', lambda:{'wheels-direction': 'west'})
        self.add_action('change-direction-south', lambda:{'wheels-direction': 'south'})

    def get_pos_x(self):
        # It must return the x coord of the agent 
        # based on the location-sensor value
        all_sensors = self.read_sensors()
        pos_x, pos_y =  all_sensors['location-sensor']
        return pos_x
    
    def get_pos_y(self):
        # It must return the y coord of the agent 
        # based on the location-sensor value
        all_sensors = self.read_sensors()
        pos_x, pos_y =  all_sensors['location-sensor']
        return pos_y
    
    def get_battery_level(self):
        # It must return the rounded (as int) sensory value 
        # from the sensor battery-level

        all_sensors = self.read_sensors()
        battery_level = all_sensors['battery-level']
        return int(battery_level)
    
    def is_out_of_charge(self):
        # It must return True if the sensor battery-level
        # is 0 and False otherwise
        if self.get_battery_level == 0:
            return True
        else:
            return False
    
    def collision_detected(self):
        # It must return the direction of the bumper
        # sensor collided with a wall if any, or None otherwise
        all_sensors = self.read_sensors()
        collision = None
        if(all_sensors['bumper-sensor-north'] == True):
            collision = 'north'
        elif(all_sensors['bumper-sensor-south'] == True):
            collision = 'south'
        elif(all_sensors['bumper-sensor-east'] == True):
            collision = 'east'
        elif(all_sensors['bumper-sensor-west'] == True):
            collision = 'west'
        
        return collision;


    # This function is already implemented
    # so you do not need to change it
    def did_collide(self):
        return False if self.collision_detected() is None else True
    
   