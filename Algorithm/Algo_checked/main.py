import sys
import argparse
from turtle import distance
from Simulator.simulator import AlgoSimulator, AlgoMinimal
from Simulator.simulator_mgr import parse_obstacle_data
from Connection.client import Client
from Connection.server import Server
from connection_to_rpi.rpi_client import RPiClient
from Settings.attributes import *

def main(simulator):
    """ simulator: Pass in True to show simulator screen
    """
    # parser = argparse.ArgumentParser(description='MDP Simulator')

    # # Add arguments
    # parser.add_argument('-a', '--arena', type=int, help='Type the index of the arena to run on', required=True)

    # args = parser.parse_args()

    # # Access the values using args
    # arena_idx = args.arena
    
    client = None

    # while True:
    try:
        # ANDROID send obstacle positions to ALGO
        print("===========================Receive Obstacles Data===========================")
        print("Waiting to receive obstacle data from ANDROID...")

        # Create a client to connect to the RPi.

        # if client is None:
        #     print(f"Attempting to connect to {RPI_HOST}:{RPI_PORT}")
        #     client = RPiClient(RPI_HOST, RPI_PORT)
        #     #  Wait to connect to RPi.
        #     while True:
        #         try:
        #             client.connect()
        #             break
        #         except OSError:
        #             pass
        #         except KeyboardInterrupt:
        #             client.close()
        #             sys.exit(1)
        #     print("Connected to RPi!\n")

        # # Wait for message from RPI
        # print("Waiting to receive data from RPi...")
        # d = client.receive_message()
        # print("Decoding data from RPi:")
        # d = d.decode("utf-8")

        # print(f'decoded msg: {d}')

        # to_return = []
        # # input conversion
        # if d[0:4] == "ALG:":
        #     d = d[4:]
        #     d = d.split(";")
        #     # now split into separate obstacles
        #     # last will be split into empty string therefore ignore
        #     for x in range(0, len(d) - 1):
        #         d_split = d[x].split(",")
        #         # d_split now holds the 4 values that are needed to create one obstacle
        #         temp = []
        #         for y in range(0, len(d_split)):
        #             # means it's x or y coordinate so multiply by 10 to correspond to correct coordinate
        #             if y <= 1:
        #                 temp.append(int(d_split[y]) * 10)
        #             elif y == 2:
        #                 if d_split[y] == "N":
        #                     temp.append(90)
        #                 elif d_split[y] == "S":
        #                     temp.append(-90)
        #                 elif d_split[y] == "E":
        #                     temp.append(0)
        #                 else:
        #                     temp.append(180)
        #             else:
        #                 temp.append(int(d_split[y]))
        #         to_return.append(temp)
        #         print("to_return: ", to_return)

        # obst_list = to_return

        print("Received all obstacles data from ANDROID.")

        print("============================Parse Obstacles Data============================")
    #     obst_list_0 =[{"x":2,"y":18,"direction":-90,"obs_id":0},
    #         {"x":6,"y":12,"direction":90,"obs_id":1},
    #         {"x":14,"y":16,"direction":180,"obs_id":3},
    #         {"x":10,"y":5,"direction":0,"obs_id":4},
    #         {"x":13,"y":2,"direction":0,"obs_id":4},
    #         {"x":18,"y":19,"direction":180,"obs_id":5}]
        
    #     obst_list_1 =[{"x":2,"y":18,"direction":-90,"obs_id":0},
    #         {"x":4,"y":8,"direction":0,"obs_id":1},
    #         {"x":10,"y":5,"direction":180,"obs_id":3},
    #         {"x":14,"y":5,"direction":90,"obs_id":4}]
        
    #     obst_list_2 =[{"x":2,"y":6,"direction":90,"obs_id":0},
    #         {"x":2,"y":18,"direction":-90,"obs_id":1},
    #         {"x":14,"y":18,"direction":180,"obs_id":3},
    #         {"x":16,"y":14,"direction":180,"obs_id":3},
    #         {"x":7,"y":8,"direction":90,"obs_id":4},
    #         {"x":13,"y":2,"direction":0,"obs_id":4},
    #         {"x":18,"y":9,"direction":-90,"obs_id":3}]
    # # [{"x":5,"y":10,"direction":0,"obs_id":0},{"x":5,"y":10,"direction":0,"obs_id":0}]
    #     if arena_idx == 0:
    #         obst_list = obst_list_0
    #     elif arena_idx == 1:
    #         obst_list = obst_list_1
    #     else:
    #         obst_list = obst_list_2
        
        obst_list = [{"x":17,"y":13,"direction":-90,"obs_id":0},
            {"x":19,"y":18,"direction":180,"obs_id":1},
            {"x":4,"y":6,"direction":90,"obs_id":2},
            {"x":5,"y":16,"direction":180,"obs_id":3},
            {"x":15,"y":8,"direction":0,"obs_id":4},
            {"x":0,"y":11,"direction":0,"obs_id":5},
            {"x":12,"y":12,"direction":-90,"obs_id":6},
            {"x":12,"y":5,"direction":-90,"obs_id":7}
            ]

        obstacles = parse_obstacle_data(obst_list)
        print(f"After parsing: {obstacles}")

        print("===============================Calculate path===============================")
        if simulator == True:
            app = AlgoSimulator(obstacles)
            app.init()
            app.execute()
            commands = app.robot.convert_commands()
            print("Full list of paths commands till last obstacle:")
            print(f"{commands}")
        else:
            app = AlgoMinimal(obstacles)
            index_list = app.execute()
            print("============================INDEX LIST===================================")
            #Adding 1 to obstacle id for it to match android
            for x in range(len(index_list)):
                index_list[x]+=1
            print(index_list)
        commands = app.robot.convert_commands()
        print("Full list of paths commands till last obstacle:")
        print(f"{commands}")

        # print("Sending list of commands to RPi...")
        # if len(commands) != 0:
        #     client.send_message(commands)
        # else:
        #     print("ERROR!! NO COMMANDS TO SEND TO RPI")

    except KeyboardInterrupt:
        client.close()
        sys.exit(1)

# Example usage:
# input_strings = ['STM|FR090', 'STM|FC050', 'STM|FL090', 'STM|FC100', 'STM|FL090', 'STM|RPI', 'STM|BC100', 'STM|BL090', 'STM|BC050', 'STM|BL090', 'STM|BR090', 'STM|RPI', 'STM|BC100', 'STM|FR090', 'STM|FC150', 'STM|BL090', 'STM|BL090', 'STM|BR090', 'STM|RPI', 'STM|FC100', 'STM|BL090', 'STM|BL090', 'STM|BC200', 'STM|BL090', 'STM|RPI', 'STM|BC100', 'STM|FL090', 'STM|FC450', 'STM|FL090', 'STM|BC100', 'STM|BR090', 'STM|RPI', 'STM|FC100', 'STM|BR090', 'STM|RPI', 'STM|BC250', 'STM|BR090', 'STM|BC150', 'STM|BR090', 'STM|BL090', 'STM|RPI', 'STM|BC050', 'STM|FL090', 'STM|FC200', 'STM|FR090', 'STM|FC350', 'STM|BL090', 'STM|RPI']
# input_strings = ['STM|FR090', 'STM|FC050', 'STM|FL090', 'STM|FC050', 'STM|FL090', 'STM|FC050', 'STM|RPI', 'STM|FC050', 'STM|BR090', 'STM|FC150', 'STM|BL090', 'STM|FC050', 'STM|FL090', 'STM|RPI', 'STM|BC050', 'STM|FL090', 'STM|FC100', 'STM|BR090', 'STM|BR090', 'STM|BL090', 'STM|RPI', 'STM|FL090', 'STM|FC100', 'STM|BR090', 'STM|FC100', 'STM|FL090', 'STM|FC100', 'STM|RPI', 'STM|BC150', 'STM|FL090', 'STM|BC050', 'STM|FR090', 'STM|BC150', 'STM|FL090', 'STM|RPI', 'STM|BC150', 'STM|FL090', 'STM|FC050', 'STM|FR090', 'STM|FC200', 'STM|FR090', 'STM|FC100', 'STM|RPI', 'STM|BC300', 'STM|FR090', 'STM|BC050', 'STM|RPI', 'STM|BC050', 'STM|FR090', 'STM|FC150', 'STM|FL090', 'STM|BC100', 'STM|BR090', 'STM|FC050', 'STM|RPI']
# mapped_strings = map_strings(input_strings)
# print(mapped_strings)

def updateRoboPos(roboPos,command):
    stmCommand = command[4:]
    print(f"Remote update of Robot: {stmCommand}")
    if(stmCommand[0:2] == "FC"):
        stmDist = int(stmCommand[2:])
        if(roboPos["direction"] == "N"):
            roboPos["y"] = roboPos["y"] + stmDist
        elif(roboPos["direction"] == "S"):
            roboPos["y"] = roboPos["y"] - stmDist
        elif(roboPos["direction"] == "E"):
            roboPos["x"] = roboPos["x"] + stmDist
        else:
            roboPos["x"] = roboPos["x"] - stmDist
    elif(stmCommand[0:2] == "BC"):
        stmDist = int(stmCommand[2:])
        if(roboPos["direction"] == "N"):
            roboPos["y"] = roboPos["y"] - stmDist
        elif(roboPos["direction"] == "S"):
            roboPos["y"] = roboPos["y"] + stmDist
        elif(roboPos["direction"] == "E"):
            roboPos["x"] = roboPos["x"] - stmDist
        else:
            roboPos["x"] = roboPos["x"] + stmDist
    elif(stmCommand[0:2] == "FR"):
        stmDist = 30
        if(roboPos["direction"] == "N"):
            roboPos["x"] = roboPos["x"] + stmDist
            roboPos["y"] = roboPos["y"] + stmDist
            roboPos["direction"] = "E"
        elif(roboPos["direction"] == "S"):
            roboPos["x"] = roboPos["x"] - stmDist
            roboPos["y"] = roboPos["y"] - stmDist
            roboPos["direction"] = "W"
        elif(roboPos["direction"] == "E"):
            roboPos["x"] = roboPos["x"] + stmDist
            roboPos["y"] = roboPos["y"] - stmDist
            roboPos["direction"] = "S"
        else:
            roboPos["x"] = roboPos["x"] - stmDist
            roboPos["y"] = roboPos["y"] + stmDist
            roboPos["direction"] = "N"
    elif(stmCommand[0:2] == "FL"):
        stmDist = 30
        if(roboPos["direction"] == "N"):
            roboPos["x"] = roboPos["x"] - stmDist
            roboPos["y"] = roboPos["y"] + stmDist
            roboPos["direction"] = "W"
        elif(roboPos["direction"] == "S"):
            roboPos["x"] = roboPos["x"] + stmDist
            roboPos["y"] = roboPos["y"] - stmDist
            roboPos["direction"] = "E"
        elif(roboPos["direction"] == "E"):
            roboPos["x"] = roboPos["x"] + stmDist
            roboPos["y"] = roboPos["y"] + stmDist
            roboPos["direction"] = "N"
        else:
            roboPos["x"] = roboPos["x"] - stmDist
            roboPos["y"] = roboPos["y"] - stmDist
            roboPos["direction"] = "S"
    elif(stmCommand[0:2] == "BR"):
        stmDist = 30
        if(roboPos["direction"] == "N"):
            roboPos["x"] = roboPos["x"] + stmDist
            roboPos["y"] = roboPos["y"] - stmDist
            roboPos["direction"] = "W"
        elif(roboPos["direction"] == "S"):
            roboPos["x"] = roboPos["x"] - stmDist
            roboPos["y"] = roboPos["y"] + stmDist
            roboPos["direction"] = "E"
        elif(roboPos["direction"] == "E"):
            roboPos["x"] = roboPos["x"] - stmDist
            roboPos["y"] = roboPos["y"] - stmDist
            roboPos["direction"] = "N"
        else:
            roboPos["x"] = roboPos["x"] + stmDist
            roboPos["y"] = roboPos["y"] + stmDist
            roboPos["direction"] = "S"
    elif(stmCommand[0:2] == "BL"):
        stmDist = 30
        if(roboPos["direction"] == "N"):
            roboPos["x"] = roboPos["x"] - stmDist
            roboPos["y"] = roboPos["y"] - stmDist
            roboPos["direction"] = "E"
        elif(roboPos["direction"] == "S"):
            roboPos["x"] = roboPos["x"] + stmDist
            roboPos["y"] = roboPos["y"] + stmDist
            roboPos["direction"] = "W"
        elif(roboPos["direction"] == "E"):
            roboPos["x"] = roboPos["x"] - stmDist
            roboPos["y"] = roboPos["y"] + stmDist
            roboPos["direction"] = "S"
        else:
            roboPos["x"] = roboPos["x"] + stmDist
            roboPos["y"] = roboPos["y"] - stmDist
            roboPos["direction"] = "N"
    else:
        pass

    if(roboPos["x"]//10 >= 19):
        roboPos["x"] = 180
    elif(roboPos["x"]//10 <= 0):
        roboPos["x"] = 10
    elif(roboPos["y"]//10 >= 19):
        roboPos["y"] = 180
    elif(roboPos["y"]//10 <= 0):
        roboPos["y"] = 10
    else:
        pass

if __name__ == '__main__':
    main(False)