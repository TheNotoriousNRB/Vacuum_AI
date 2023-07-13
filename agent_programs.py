import math
import random 
import numpy as np

from une_ai.vacuum import DISPLAY_HEIGHT, DISPLAY_WIDTH, TILE_SIZE
from une_ai.models import GridMap
from vacuum_agent import VacuumAgent

DIRECTIONS = VacuumAgent.WHEELS_DIRECTIONS

"""
Test agent:
- If the vacuum power is off, it starts cleaning
- At each time, it chooses a random direction for the wheels
"""
def test_behaviour(percepts, actuators):
    actions = []
    if actuators['vacuum-power'] != 1:
        actions.append('start-cleaning')
    
    new_direction = random.choice(DIRECTIONS)
    actions.append('change-direction-{0}'.format(new_direction))

    return actions

#Function - change_direction
#takes a parameter old_direction and returns a random DIRECTION
#excluding old_direction
def change_direction(old_direction):
    new_direction = random.choice(DIRECTIONS)
    while old_direction == random.choice(DIRECTIONS):
        new_direction = random.choice(DIRECTIONS)
    return new_direction;


"""
Simple reflex agent: 
- If the vacuum power is off, it starts cleaning
- If there is dirt on the current tile (i.e. 'dirt-sensor-center'), 
it activates the suction mechanism
- If the agent hits a wall, it changes the direction of the wheels randomly
- If the agent senses dirt on the surrounding tiles, 
it changes the direction of the wheels towards the dirt
"""
def simple_reflex_behaviour(percepts, actuators):
    actions = []
    if actuators['vacuum-power'] != 1:
        actions.append('start-cleaning')
    
    if percepts['dirt-sensor-center'] == True:
        actions.append('activate-suction-mechanism')
    elif actuators['suction-power'] == 1:
        actions.append('deactivate-suction-mechanism')

    cur_direction = actuators['wheels-direction']
    new_direction = cur_direction
    if percepts['bumper-sensor-{0}'.format(cur_direction)] == True:
        directions = DIRECTIONS.copy()
        directions.remove(cur_direction)
        new_direction = random.choice(directions)

    for dir in DIRECTIONS:
        if percepts['dirt-sensor-{0}'.format(dir)] == True:
            new_direction = dir
            break

    if new_direction != cur_direction:
        actions.append('change-direction-{0}'.format(new_direction))

    return actions


"""
Model-based reflex agent: 
- The agent keeps track of the walls it crashed against by using a GridMap
- Based on the current wheels direction, if the next tile is a wall,
the agent will change direction
- In all the other situations, the agent will behave like the simple-reflex agent
"""
w_env = math.floor(DISPLAY_WIDTH/TILE_SIZE)
h_env = math.floor(DISPLAY_WIDTH/TILE_SIZE)
environment_map = GridMap(w_env, h_env, False)

def future_state(model, cur_location, cur_direction):
    offset = {
        'north' : (0, -1),
        'south' : (0, 1),
        'east' : (1, 0),
        'west' : (-1, 0)
    }
    cur_x, cur_y = cur_location
    #future location
    new_x, new_y = (cur_x + offset[cur_direction][0], cur_y+offset[cur_direction][1])

    try:
        value = model.get_item_value(new_x, new_y)
        new_location = (new_x, new_y)
    except:
        #If here, then the next location is out of bounds
        #Assume it as a wall. 
        value = 'W'
        new_location = None

    return value, new_location

def model_based_reflex_behaviour(percepts, actuators):
    #Model Based reflex agent initialized!
    actions = simple_reflex_behaviour(percepts, actuators)

    cur_location = percepts['location-sensor']
    cur_direction = actuators['wheels-direction']

    #In case of collision detected
    #Update the eivironment model
    if percepts['bumper-sensor-{0}'.format(cur_direction)] == True:
        #Get the next location
        _ , future_location = future_state(environment_map, cur_location, cur_direction)
        #If the location is out of bounds, set it as a Wall in the model
        if future_location is not None:
            environment_map.set_item_value(future_location[0], future_location[1], 'W')
    
    #Check if there is any change-direction action from the simple_reflex_behaviour
    new_direction = cur_direction
    for action in actions:
        if action.startswith('change-direction'):
            token = action.split('-')
            new_direction = token[2]
            actions.remove(action)
    
    valid_directions = []
    #For each direction, check if there is any wall
    for direction in DIRECTIONS:
        future_state_value, _ = future_state(environment_map, cur_location, direction)
        #If there is no wall, it can be a valid choice for direction
        if future_state_value != 'W':
            valid_directions.append(direction)
    
    #Check if direction obtained from simple_reflex_behaviour is valid
    if new_direction not in valid_directions:
        new_direction = random.choice(valid_directions)

    #If we've changed the direction, append action to change the direction
    if new_direction != cur_direction:
        actions.append('change-direction-{0}'.format(new_direction))

    return actions

"""
Goal-based agent:
- The agent keeps track of previously explored tiles by using a GridMap
- Based on the current wheels direction, if the next tile was already explored,
the agent will change direction towards an unexplored tile (if any, otherwise 
it will proceed in the same direction)
- In all the other situations, the agent will behave like the model-based reflex agent
- The agent will stop cleaning once the environment is fully explored
"""
def goal_based_behaviour(percepts, actuators):
    actions = []

    return actions

"""
Utility-based agent:
The agent also stores information about dirt on the adjacent cells detected by the dirt sensors.
The agent then chooses the next direction via a utility function.
This utility function takes a direction as input, and implement the following steps:
- The agent examines its internal model of the world and retrieves a list of cell values 
in the specified direction.
- It filters out any cells that are obstructed by a wall, considering only the unobstructed cells.
- If there is dirt in the considered direction, the utility is returned as a high value such as 999
otherwise
- The agent calculates the minimum distance (min_dist) from an unexplored cell in this 
filtered list. If there are no unexplored cells, min_dist is set to a high value such as 999.
- The utility value is determined as -1 multiplied by min_dist, 
reflecting the notion that the agent values smaller distances to unexplored cells.
"""
def utility_based_behaviour(percepts, actuators):
    actions = []
    
    return actions
    