import json
import time
from turtle import distance
from Simulator.simulator import AlgoSimulator, AlgoMinimal
from Simulator.simulator_mgr import parse_obstacle_data
from Connection.client import Client
from Connection.server import Server


def main(simulator):
    """ simulator: Pass in True to show simulator screen
    """


    index = 0
    t=3

    i = 0
    reverse = "STM|BC010"
    scan = "STM|RPI"
    forward = "STM|FC010"
    reverseSecond = "STM|BC010"
    forwardSecond = "STM|FC030"
    #obst_list = []
    image_ids = ["11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
                 "21", "22", "23", "24", "25", "26", "27", "28", "29", "30",
                 "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40"]


    # Create a client to send and receive information from the RPi
    server = Server("192.168.36.25", 3004)  # 10.27.146 139 | 192.168.13.1
    server.start()
    #client.connect()

    while True:
        try:
            # ANDROID send obstacle positions to ALGO
            print("===========================Receive Obstacles Data===========================")
            print("Waiting to receive obstacle data from ANDROID...")
            obstacle_data = server.receive()
            obst_list = json.loads(obstacle_data)
            print(obst_list)




           # while obstacle_data != "PC;START":
            #    obstacle_data = server.receive()
             #   if obstacle_data == "PC;START":
              #      break
              #  data = json.loads(obstacle_data)
              #  print(data)
             #   obst_list.append(data)
              #  i+=1

           # obst_list.pop()
            print("Received all obstacles data from ANDROID.")
            print(f"Obstacles data: {obst_list}")

            print("============================Parse Obstacles Data============================")
            # obst_list =[{"x":1,"y":18,"direction":-90,"obs_id":0},
            #   {"x":6,"y":12,"direction":90,"obs_id":1},
            #   {"x":14,"y":16,"direction":180,"obs_id":3},
            #   {"x":10,"y":6,"direction":0,"obs_id":4},
            #   {"x":13,"y":2,"direction":0,"obs_id":4},
            #   {"x":18,"y":19,"direction":180,"obs_id":5}]
        # [{"x":5,"y":10,"direction":0,"obs_id":0},{"x":5,"y":10,"direction":0,"obs_id":0}]



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



            # 5,4,3,2,1,0


            print("=======================Send path commands to move to obstacles=======================")
            server.send("STM|FC000")
            time.sleep(t)
            clen =len(commands)
            for x ,command in enumerate(commands):
                print(command)
                server.send(command)
                print(f"Sending path commands to move to obstacle {index_list[index]} to RPI to STM...")

                if (x<clen-1):
                    if (commands[x+1]== 'STM|RPI'):
                        if(commands[x]== 'STM|BR090' or commands[x]== 'STM|BL090'or commands[x]== 'STM|FL090' or commands[x]== 'STM|FR090'):
                            time.sleep(3*t)
                        else:
                            time.sleep(t)
                    else:
                        time.sleep(t / 3 * 2)
                else:
                    time.sleep(t)

                #if(command != "RPI|"):
                    #updateRoboPos(roboPosCoor, command)
                   # roboUpdateToAndroid = f"AND|ROBOT,<{roboPosCoor['x']//10}>,<{roboPosCoor['y']//10}>,<{roboPosCoor['direction']}>"
                    #print("--------")
                    #print(roboUpdateToAndroid)
                    #server.send(roboUpdateToAndroid)
                    #time.sleep(1)

                if command == "STM|RPI":
                    print("Waiting to receive image_id from STM/IMAGE REC")
                    var = server.receive()
                    if var in image_ids:
                        s = "AND|TARGET,"
                        s+=str(index_list[index])
                        s+=","
                        s+=var
                        index+=1
                        print(s)
                        server.send(s)
                    else:
                        print("Moving backwards")
                        time.sleep(t)
                        server.send(reverse)
                        print(reverse)
                        time.sleep(t)
                        server.send(scan)
                        print(scan)
                        print("Waiting to receive image_id from STM/IMAGE REC")
                        var = server.receive()

                        if var in image_ids:
                            s = "AND|TARGET,"
                            s+=str(index_list[index])
                            s+=","
                            s+=var
                            index+=1
                            print(s)
                            server.send(s)
                        print("Moving Forward to offset")
                        server.send(forward)
                        # time.sleep(t)




        except KeyboardInterrupt:
            server.close()

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