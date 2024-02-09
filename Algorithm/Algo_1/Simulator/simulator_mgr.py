import json
from typing import List
from Map.obstacle import Obstacle
from Settings.attributes import *

def parse_obstacle_data(data) -> List[Obstacle]:
    obs = []
    lst3 = []
    lst = []
    i = 0

    for obj in data:
        lst.append(obj)

    for i in lst:
        i["x"] = (GRID_CELL_LENGTH / 2 + GRID_CELL_LENGTH * i["x"]) / SCALING_FACTOR
        i["y"] = (GRID_CELL_LENGTH / 2 + GRID_CELL_LENGTH * i["y"]) / SCALING_FACTOR
        i["obs_id"] -= 1

    a = [list(row) for row in zip(*[m.values() for m in lst])]

    for i in range(len(a[0])):
        lst2 = [item[i] for item in a]
        lst3.append(lst2)
        i+=1

    for obstacle_params in lst3:
        obs.append(Obstacle(obstacle_params[0],
                            obstacle_params[1],
                            Direction(obstacle_params[2]),
                            obstacle_params[3]))

    # [[x, y, orient, index], [x, y, orient, index]]
    return obs
