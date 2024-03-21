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
            print("simple: ")
            print(simple)
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
        max_obs_visited_commands = deque()
        max_obs_visited_count = 0
        # for i in range(len(simple_hamiltonians)):
        for i in range(MAX_RETRY):
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
                scan_count = self.count_scan_commands(self.commands)
                if scan_count > max_obs_visited_count:
                    max_obs_visited_count = scan_count
                    max_obs_visited_commands = self.commands
                continue
            self.compress_paths()
            print("-" * 70)

            return index_list
        
        print()
        print("-" * 70)
        print("NO COMPLETE PATH FOUND!!!")
        print("-" * 70)
        print()
        
        # if no path found then fall back to the best path and ignore the inaccessible ones
        # index_list = index_lists[0]
        # self.simple_hamiltonian = simple_hamiltonians[0]
        # self.commands = deque()
        # for obstacle in self.simple_hamiltonian:
        #     target = obstacle.get_robot_target_pos()
        #     print("-" * 70)
        #     print(f"Planning {curr} to {target}")
        #     res = ModifiedAStar(self.grid, self, curr, target).start_astar()
        #     if res is None:
        #         print(f"No path found from {curr} to {obstacle}")
        #         print(f"Abandoning {obstacle}!!")
        #     else:
        #         print("Path found.")
        #         curr = res
        #         self.commands.append(ScanCommand(ROBOT_SCAN_TIME, obstacle.index))

        self.commands = max_obs_visited_commands
        print("self.commands: ",self.commands)
        self.compress_paths()
        print("-" * 70)

        return index_list
    
    def count_scan_commands(self, deque_instance):
        return sum(isinstance(item, ScanCommand) for item in deque_instance)