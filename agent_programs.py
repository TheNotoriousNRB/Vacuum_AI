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
    else:
        actions.append('deactivate-suction-mechanism')
    
    if percepts['bumper-sensor-north'] == True:
        new_direction = change_direction('north')
        print(new_direction)
        actions.append('change-direction-{0}'.format(new_direction))

    if percepts['bumper-sensor-south'] == True:
        new_direction = change_direction('south')
        actions.append('change-direction-{0}'.format(new_direction))

    if percepts['bumper-sensor-east'] == True:
        new_direction = change_direction('east')
        actions.append('change-direction-{0}'.format(new_direction))

    if percepts['bumper-sensor-west'] == True:
        new_direction = change_direction('west')
        actions.append('change-direction-{0}'.format(new_direction))

    if percepts['dirt-sensor-north'] == True:
        actions.append('change-direction-north')
    
    if percepts['dirt-sensor-east'] == True:
        actions.append('change-direction-east')
    
    if percepts['dirt-sensor-west'] == True:
        actions.append('change-direction-west')
    
    if percepts['dirt-sensor-south'] == True:
        actions.append('change-direction-south')

    return actions



"""
Model-based reflex agent: 
- The agent keeps track of the walls it crashed against by using a GridMap
- Based on the current wheels direction, if the next tile is a wall,
the agent will change direction
- In all the other situations, the agent will behave like the simple-reflex agent
"""
def model_based_reflex_behaviour(percepts, actuators):
    actions = []

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
    