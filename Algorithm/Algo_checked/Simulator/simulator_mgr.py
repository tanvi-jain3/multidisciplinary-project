import json
from typing import List
from Map.obstacle import Obstacle
from Settings.attributes import *

def parse_obstacle_data(data) -> List[Obstacle]:
    obs = []
    lst3 = []
    lst = []
    i = 0

    print("obs_data: ", data)

    for obj in data:
        if len(obj) < 4:
            continue
        lst.append(obj)

    print("lst: ", lst)

    for i in lst:
        i[0] = (GRID_CELL_LENGTH / 2 + GRID_CELL_LENGTH * (i[0] // 10) ) / SCALING_FACTOR
        i[1] = (GRID_CELL_LENGTH / 2 + GRID_CELL_LENGTH * (i[1] // 10)) / SCALING_FACTOR
        # i[3] -= 1

    a = [list(row) for row in zip(*[m for m in lst])]

    print("a: ", a)

    for i in range(len(a[0])):
        lst2 = [item[i] for item in a]
        lst3.append(lst2)
        i+=1

    print("lst2: ", lst2)
    print("lst3: ", lst3)

    for obstacle_params in lst:
        print("obs_to_be_appended: ", obstacle_params)
        obs.append(Obstacle(obstacle_params[0],
                            obstacle_params[1],
                            Direction(obstacle_params[2]),
                            obstacle_params[3]))

    # [[x, y, orient, index], [x, y, orient, index]]
    return obs