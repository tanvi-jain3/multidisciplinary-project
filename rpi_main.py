#!/usr/bin/env python3
import sys
import configparser
import wlan
import time
import connSerial
import str2list
import mdpRobot
import translator
import take_pic
import subprocess
import random
import myLED

def estBluetooth():
    while(True):
        try:
            print("Checking Bluetooth connection...")
            bluetooth = connSerial.Serial(interface="/dev/rfcomm0")
            print("Bluetooth successfully connected")
            return bluetooth
        except Exception as e:
            print("Bluetooth not connected... Enabling Discovery mode...")
            subprocess.call(['sudo', 'hciconfig', 'hci0', 'piscan'])
            time.sleep(5)

def estUSB():
    while(True):
        try:
            print("Checking USB connection...")
            usb = connSerial.Serial(interface="/dev/ttyUSB0", baud=115200)
            print("USB successfully connected")
            return usb
        except Exception as e:
            print("USB not connected... Retrying in 5 seconds")
            time.sleep(5)

def estWifi(host, port):
    while(True):
        try:
            print("Establishing connection with Laptop")
            wifi = wlan.Wlan(host=host, port=port)
            result = wifi.start_client()
            if(result != 0):
                return wifi
            else:
                print("Reconnecting to Server")
                time.sleep(5) 
        except Exception as e:
            print("Unable to establish connection with Server")
            time.sleep(5)
        
def main():
    try:
        # Initial Variables
        config = configparser.ConfigParser()
        config.read("config.ini")
        
        host = config.get("variables", "LAPTOP_HOST")
        port = int(config.get("variables", "LAPTOP_PORT"))
        
        # Object declarations
        myRobot = mdpRobot.Robot()
        bluetooth = estBluetooth() 
        usb = estUSB() 
        green = myLED.myLED(gpioPin=23, power=1)
        red = myLED.myLED(gpioPin=24, power=10)
        wifi = estWifi(host=host, port=port)
        
        # String to listen for when STM finishes command
        STMEND = "Movement Done!" 
        
        # obstacles = [[135, 25, 0, 1], [55, 75, -90, 2], [195, 95, 180, 3], [175, 185, -90, 4], [75, 125, 90, 5], [15, 185, -90, 6]]
        obstacles = []
        while True:
            green.up()
            bluetooth.send_command(command="STATUS/Ready to start")
            command = bluetooth.receive_command()   # Listening for Bluetooth Commands
            green.down()
            red.up()
            command = command.split('/')
            instruction = command.pop(0)
            
            # Obstacle paths
            if(instruction == "START"):
                task = command.pop(0)
                
                # Task 01
                if(task == "EXPLORE"): # EXAMPLE: "START/EXPLORE/(R,04,03,0)/(00,08,10,90)/(01,12,06,-90)"
                    robot_pos = command.pop(0).replace("(", "").replace(")", "").split(",")
                    myRobot.robot_pos(delta_x=int(robot_pos[1]), delta_y=int(robot_pos[2]))
                    bluetooth.send_command(command=myRobot.get_coords())
                    
                    obstacles = translator.android2clientTranslate(obs_data=command)
                    
                    wifi.main(obstacles=obstacles) #Connect to Laptop and send obstacle data
                    # after this part, we will receive data from the client
                    # assuming data is in list format and returning [['w030'], ['e090'], ['w050'], ['d000'], ['p001']]
                    path = wifi.receive_data()
                    
                    obs_path = path.pop(0)
                    
                    while True:
                        if(len(obs_path) == 0) or (len(path)==0):
                            break
                        time.sleep(0.1)
                        bluetooth.send_command(command=f"STATUS/Looking for target {obs_path[0]}")
                        for i in range(len(path)):
                            movement = path.pop(0)
                            move, val1, val2 = translator.client2stmTranslate(movement)
                            
                            # Take picture command
                            if(move == 7):
                                successRecognition = False
                                recognitionFailed = 0
                                while((not successRecognition) and (recognitionFailed < 2)):
                                    result = take_pic.main()
                                    # result = "-1"
                                    # Target found!
                                    if(result != "-1"):
                                        myLED.myLED.picTaken()
                                        bluetooth.send_command(command=f"TARGET/{obs_path[0]}/{result}")
                                        time.sleep(0.1)
                                        successRecognition = True # Mark as success
                                    
                                    else:
                                        bluetooth.send_command(command=f"TARGET/{obs_path[0]}/{result}")
                                        time.sleep(0.1)
                                        recognitionFailed += 1
                                        # correctional movements
                                        if(recognitionFailed < 2):
                                            usb.send_stm_command_axis(move=2, x=0, y=-(10 * recognitionFailed))
                                            myRobot.update_delta_straight(movement=2, distance=(10 * recognitionFailed))
                                            
                                            command = usb.receive_stm_command()
                                            bluetooth.send_command(command=myRobot.get_coords())
                                
                                if(recognitionFailed == 2):
                                    recognitionFailed -= 1
                                    
                                for i in range(recognitionFailed, 0, -1):
                                    usb.send_stm_command_axis(move=1, x=0, y=(10 * i))
                                    myRobot.update_delta_straight(movement=1, distance=(10 * i))
                                    
                                    command = usb.receive_stm_command()
                                    bluetooth.send_command(command=myRobot.get_coords())
                                
                                obs_path.pop(0)        
                                break # Breaks out from the for loop and start from line 92
                            
                            # Turning command
                            elif(val2 is None):
                                usb.send_stm_command_angle(move, val1)
                                myRobot.update_delta_turn(movement=move, angle=val1)
                            
                            # Straight command
                            else:
                                if(move == 2):
                                    usb.send_stm_command_axis(move, val1, -val2)
                                else:
                                    usb.send_stm_command_axis(move, val1, val2)

                                myRobot.update_delta_straight(movement=move, distance=val2)
                            
                            command = usb.receive_stm_command()
                            bluetooth.send_command(command=myRobot.get_coords())
                            time.sleep(0.1)
                    time.sleep(0.2)
                    bluetooth.send_command(command="FINISH/EXPLORE")
                    time.sleep(1)
                    # bluetooth.send_command(command="FINISH/EXPLORE")
                    # time.sleep(0.1)

                elif(task == "SIMULATOR"): # EXAMPLE: "START/SIMULATOR/(R,04,03,0)/(00,08,10,90)/(01,12,06,-90)"
                    robot_pos = command.pop(0).replace("(", "").replace(")", "").split(",")
                    myRobot.robot_pos(delta_x=int(robot_pos[1]), delta_y=int(robot_pos[2]))
                    bluetooth.send_command(command=myRobot.get_coords())
                    
                    obstacles = translator.android2clientTranslate(obs_data=command)
                    
                    wifi.main(obstacles=obstacles) #Connect to Laptop and send obstacle data
                           
                # Task 02
                elif(task == "PATH"):
                    bluetooth.send_command(command="STATUS/TASK #02")
                    usb.send_stm_command_axis(move=10)
                    command = usb.receive_stm_command()

                    obs_counter = 0
                    while(obs_counter != 2):
                        # take photo
                        recognitionFailed = 0
                        while(True and (recognitionFailed < 2)):
                            time.sleep(0.5)
                            result = take_pic.main() # Result of the image recognition
                            
                            if(result == "39"):
                                for i in range(recognitionFailed, 0, -1):
                                    usb.send_stm_command_axis(move=1, x=0, y=(10 * i))
                                    myRobot.update_delta_straight(movement=1, distance=(10 * i))
                                    command = usb.receive_stm_command()
                                
                                recognitionFailed = 0
                                
                                if(obs_counter < 1):
                                    usb.send_stm_command_axis(move=11)
                                    command = usb.receive_stm_command()
                                elif(obs_counter < 2):
                                    usb.send_stm_command_axis(move=13)
                                    command = usb.receive_stm_command()
                                
                                break
                            
                            elif(result == "38"):
                                for i in range(recognitionFailed, 0, -1):
                                    usb.send_stm_command_axis(move=1, x=0, y=(10 * i))
                                    myRobot.update_delta_straight(movement=1, distance=(10 * i))
                                    command = usb.receive_stm_command()

                                recognitionFailed = 0
                                
                                if(obs_counter < 1):
                                    usb.send_stm_command_axis(move=12)
                                    command = usb.receive_stm_command()
                                elif(obs_counter < 2):
                                    usb.send_stm_command_axis(move=14)
                                    command = usb.receive_stm_command()
                                
                                # if(obs_counter < 1):
                                #     usb.send_stm_command_task02(move=10)
                                #     command = usb.receive_stm_command()
                                    
                                break
                            else:
                                recognitionFailed += 1
                                
                                if(recognitionFailed < 2):
                                    usb.send_stm_command_axis(move=2, x=0, y=-(10 * recognitionFailed))
                                    myRobot.update_delta_straight(movement=2, distance=(10 * recognitionFailed))
                                    
                                    command = usb.receive_stm_command()
                        
                        if(recognitionFailed == 2):
                            recognitionFailed -= 1
                            
                        for i in range(recognitionFailed, 0, -1):
                            usb.send_stm_command_axis(move=1, x=0, y=(10 * i))
                            myRobot.update_delta_straight(movement=1, distance=(10 * i))
                            command = usb.receive_stm_command()
                            
                            if(obs_counter == 0):
                                usb.send_stm_command_axis(move=random.randint(11,12))
                            
                            elif(obs_counter == 1):
                                usb.send_stm_command_axis(move=random.randint(13,14))
                                command = usb.receive_stm_command()
                            
                        obs_counter += 1
                    
                    # Fianl command to receive
                    bluetooth.send_command(command="FINISH/PATH")
                    time.sleep(1)
                       
            # Manual Movements
            elif(instruction == "MOVE"):
                direction = command.pop(0)
                
                bluetooth.send_command(command="STATUS/Sending command to STM")
                if(direction == "F"):
                    usb.send_stm_command_axis(move=1, x=0, y=10)
                    myRobot.update_delta_straight(movement=1, distance=10)
                    
                elif(direction == "B"):
                    usb.send_stm_command_axis(move=2, x=0, y=-10)
                    myRobot.update_delta_straight(movement=2, distance=10)
                    
                elif(direction == "L"):
                    usb.send_stm_command_angle(move=3, angle=90)
                    myRobot.update_delta_turn(movement=3, angle=90)
                
                elif(direction == "R"):
                    usb.send_stm_command_angle(move=4, angle=90)
                    myRobot.update_delta_turn(movement=4, angle=90)

                elif(direction == "BL"):
                    usb.send_stm_command_angle(move=5, angle=90)
                    myRobot.update_delta_turn(movement=5, angle=90)

                elif(direction == "BR"):
                    usb.send_stm_command_angle(move=6, angle=90)
                    myRobot.update_delta_turn(movement=6, angle=90)
                    
                command = usb.receive_stm_command()
                bluetooth.send_command(command=myRobot.get_coords())

            # Stop Instruction
            elif(instruction == "STOP"):
                bluetooth.send_command(command="STOP")

            # Task A.3
            elif(instruction == "CUSTOMMOVE"): # "CUSTOMMOVE/F/90"
                direction = command.pop(0)
                
                bluetooth.send_command(command="STATUS/Sending command to STM")
                
                distance = command.pop(0)
                
                if(direction == "F"):    
                    usb.send_stm_command_axis(move=1, x=0, y=int(distance))
                    myRobot.update_delta_straight(move=1, distance=int(distance))
                elif(direction == "B"):
                    usb.send_stm_command_axis(move=2, x=0, y=int(-distance))
                    myRobot.update_delta_straight(move=2, distance=int(distance))
                
                command = usb.receive_stm_command()
                bluetooth.send_command(command=myRobot.get_coords())
                    
            # Task A.4
            elif(instruction == "CUSTOMTURN"): # "CUSTOMTURN/L/180"
                direction = command.pop(0)
                
                bluetooth.send_command(command="STATUS/Sending command to STM")
                
                angle = command.pop(0)
                
                if(direction == "L"):
                    usb.send_stm_command_angle(move=3, angle=int(angle))
                    myRobot.update_delta_turn(movement=3, angle=int(angle))
                
                elif(direction == "R"):
                    usb.send_stm_command_angle(move=4, angle=int(angle))
                    myRobot.update_delta_turn(movement=4, angle=int(angle))

                elif(direction == "BL"):
                    usb.send_stm_command_angle(move=5, angle=int(angle))
                    myRobot.update_delta_turn(movement=5, angle=int(angle))

                elif(direction == "BR"):
                    usb.send_stm_command_angle(move=6, angle=int(angle))
                    myRobot.update_delta_turn(movement=6, angle=int(angle))
                
                command = usb.receive_stm_command()
                bluetooth.send_command(command=myRobot.get_coords())

            # Task A.5    
            elif(instruction == "BULLSEYE"): # "BULLSEYE"
                while(True):                
                    result = take_pic.main() # Result of the image recognition
                    
                    # Task A.5
                    # separate this from task 01
                    if(result == 'bullseye'):
                        fixed_commands = ["a090", "w060", "q090", "q090"] #[-2] w010
                        for command in fixed_commands:
                            tmpMove, tmpVal1, tmpVal2 = translator.client2stmTranslate(command)
                            
                            # Turning command
                            if(tmpVal2 is None):
                                usb.send_stm_command_angle(tmpMove, tmpVal1)
                                myRobot.update_delta_turn(movement=tmpMove, angle=tmpVal1)

                            # Straight command
                            else:
                                if(tmpMove == 2):
                                    usb.send_stm_command_axis(tmpMove, tmpVal1, -tmpVal2)
                                else:
                                    usb.send_stm_command_axis(tmpMove, tmpVal1, tmpVal2)
                                myRobot.update_delta_straight(movement=tmpMove, distance=tmpVal2)
                            
                            command = usb.receive_stm_command()
                            bluetooth.send_command(command=myRobot.get_coords())
                    
                    else:
                        break
                    
                print("NO BULLSEYE")
                command = usb.receive_stm_command()
                bluetooth.send_command(command=myRobot.get_coords())
                break
            
            red.down()
    except KeyboardInterrupt:
        print("Keyboard interrupt detected...  Closing all connections")
        bluetooth.close()
        usb.close()
        wifi.close()
        myLED.myLED.close()

    except Exception as e:
        print("ERROR")
        print(e)
        print("Closing all connections")
        bluetooth.close()
        usb.close()
        wifi.close()
        myLED.myLED.close()
    
if __name__ == '__main__':
    while(True):
        main()
        time.sleep(5)
