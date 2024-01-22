import itertools
import math
import sys
from collections import deque
from typing import Tuple
from Map.obstacle import Obstacle
from Robot.commands import *
from Settings.attributes import *
from Robot.path_algo import ModifiedAStar


class Brain:
    def __init__(self, robot, grid):
        self.robot = robot
        self.grid = grid

        # Compute the simple Hamiltonian path for all obstacles
        self.simple_hamiltonian = tuple()

        # Create all the commands required to finish the course.
        self.commands = deque()


    def compute_simple_hamiltonian_path(self) -> Tuple[Obstacle]:

        # Generate all possible sequences of obstacles
        perms = list(itertools.permutations(self.grid.obstacles))

        index_list = [[] for i in range(len(perms))]
        # Get the path that has the least distance travelled.
        def calc_distance(path):
            # Create all target points, including the start.
            targets = [self.robot.pos.xy_pygame()]

            for obstacle in path:
                targets.append(obstacle.pos.xy_pygame())

            dist = 0
            for i in range(len(targets) - 1):
                dist += math.sqrt(((targets[i][0] - targets[i + 1][0]) ** 2) +
                                  ((targets[i][1] - targets[i + 1][1]) ** 2))
            return dist

        perms.sort(key=calc_distance)
        print("Found a simple hamiltonian path:")
        for i, simple in enumerate(perms):

            for ob in simple:
                # print(i, index_list)
                # print(ob.getIndex())
                index_list[i].append(ob.getIndex())
                #print(f"{ob}")
        # print(perms)
        return perms, index_list

    def compress_paths(self):
        print("Compressing commands... ", end="")
        index = 0
        new_commands = deque()
        while index < len(self.commands):
            command = self.commands[index]
            if isinstance(command, StraightCommand):
                new_length = 0
                while index < len(self.commands) and isinstance(self.commands[index], StraightCommand):
                    new_length += self.commands[index].dist
                    index += 1
                command = StraightCommand(new_length)
                new_commands.append(command)
            else:
                new_commands.append(command)
                index += 1
        self.commands = new_commands
        print("Done!")

    def plan_path(self):
        print("-" * 70)
        print("Starting path computation...")
        simple_hamiltonians, index_lists = self.compute_simple_hamiltonian_path()
        for i in range(len(simple_hamiltonians)):
            not_found = 0
            self.simple_hamiltonian = simple_hamiltonians[i]
            self.commands = deque()
            index_list = index_lists[i]
            curr = self.robot.pos.copy()  # We use a copy rather than get a reference.
            for obstacle in self.simple_hamiltonian:
                target = obstacle.get_robot_target_pos()
                print("-" * 70)
                print(f"Planning {curr} to {target}")
                res = ModifiedAStar(self.grid, self, curr, target).start_astar()
                if res is None:
                    not_found = 1
                    print(f"No path found from {curr} to {obstacle}")
                    break
                else:
                    print("Path found.")
                    curr = res
                    self.commands.append(ScanCommand(ROBOT_SCAN_TIME, obstacle.index))
            if not_found:
                continue
            self.compress_paths()
            print("-" * 70)

            return index_list
        index_list = index_lists[0]
        self.simple_hamiltonian = simple_hamiltonians[0]
        self.commands = deque()
        for obstacle in self.simple_hamiltonian:
            target = obstacle.get_robot_target_pos()
            print("-" * 70)
            print(f"Planning {curr} to {target}")
            res = ModifiedAStar(self.grid, self, curr, target).start_astar()
            if res is None:
                print(f"No path found from {curr} to {obstacle}")
            else:
                print("Path found.")
                curr = res
                self.commands.append(ScanCommand(ROBOT_SCAN_TIME, obstacle.index))
        self.compress_paths()
        print("-" * 70)

        return index_list


    def compute_simple_hamiltonian_path1(self) -> Tuple[Obstacle]:

        # Generate all possible permutations for the image obstacles
        perms = list(itertools.permutations(self.grid.obstacles))

        index_list = []

        # Get the path that has the least distance travelled.
        def calc_path_cost(path):
            # Create all target points, including the start.
            targets = [self.robot.pos.copy()]
            for obstacle in path:
                targets.append(obstacle.get_robot_target_pos())
            dist = 0
            cost = 0
            for i in range(len(targets) - 1):
                inital = ModifiedAStar(self.grid, self, targets[i], targets[i+1])
                res = inital.start_astar()
                if res is None:
                    print(f"No path found from {targets[i]} to {targets[i+1]}")
                    cost = 99999 # choose a large number, so that the algo won't enfavour this path
                    break
                else:
                    cost += inital.getTotalCost()
                current_target_x, current_target_y = targets[i].xy_pygame()
                next_target_x, next_target_y = targets[i+1].xy_pygame()
                dist += math.sqrt(((current_target_x - next_target_x) ** 2) +
                                  ((current_target_y - next_target_y) ** 2))
            return dist+cost

        simple = min(perms, key=calc_path_cost)

        print("Found a simple hamiltonian path:")
        for ob in simple:
            index_list.append(ob.getIndex())
            print(f"{ob}")
        return simple, index_list

