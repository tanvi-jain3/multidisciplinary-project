from Settings.config import *
from enum import Enum


class Direction(Enum):
    LEFT = 180
    TOP = 90
    BOTTOM = -90
    RIGHT = 0

# Robot Attributes
ROBOT_START_X = 15 * SCALING_FACTOR
ROBOT_START_Y = 15 * SCALING_FACTOR
ROBOT_LENGTH = 20 * SCALING_FACTOR  # robot footprint setted as 20 * 20(recommended 30 * 30)
ROBOT_TURN_RADIUS = 20 * SCALING_FACTOR
ROBOT_TURN_RADIUS_DRIFT = 30 * SCALING_FACTOR
ROBOT_SPEED_PER_SECOND = 30 * SCALING_FACTOR
ROBOT_S_FACTOR = ROBOT_LENGTH / ROBOT_TURN_RADIUS
ROBOT_SAFETY_DISTANCE = 15* SCALING_FACTOR
ROBOT_SCAN_TIME = 0.25  # Time provided for scanning an obstacle image in seconds.

# Grid Attributes
GRID_LENGTH = 200 * SCALING_FACTOR  # Movement area is 200cm by 200cm
GRID_CELL_LENGTH = 10 * SCALING_FACTOR  # Grid cell is 10cm by 10cm
GRID_START_BOX_LENGTH = 30 * SCALING_FACTOR  # Recommended starting area is 40cm by 40cm
GRID_NUM_GRIDS = GRID_LENGTH // GRID_CELL_LENGTH  # Number of grid cells

# Obstacle Attributes
OBSTACLE_LENGTH = 10 * SCALING_FACTOR  # Obstacle is 10cm by 10cm
OBSTACLE_SAFETY_WIDTH = ROBOT_SAFETY_DISTANCE + OBSTACLE_LENGTH // 2  # With respect to the center of the obstacle

# Path Finding Attributes
PATH_TURN_COST = 999 * ROBOT_SPEED_PER_SECOND * ROBOT_TURN_RADIUS
PATH_TURN_CHECK_GRANULARITY = 1