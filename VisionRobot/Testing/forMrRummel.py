from __future__ import print_function, division #importing the ability to customize the terminal 
from builtins import input

from gopigo import * #imports the gopigo library
import pygame #for the ps4 controls
import sys #imports the system
import os 
import picamera #imports picamera
import time #allows for delays 

#-----Console Menu------
#these are the controls for the robot
def print_ps4Menu(): #PS4 controler controls
	print
	print("  Controls")
	print
	print("  Left Joystick to dive motors")
	print("  Right Joystick to control servo")
	print("  Press square to take photo")
	
def take_photo(): #takes a picture and closes the camera
	camera = picamera.PiCamera()
	camera.capture('image.jpg')
	camera.close()
	print("\n    You just took a photo")

def set_servo(): #sets the servo at 90 degrees 
	servo(90)
	time.sleep(.1)
	disable_servo()
	print("90")

def PygameSetup(): #sets up pygame for the joystick
	pygame.init()
	size = [500, 700]
	screen = pygame.display.set_mode(size)

	pygame.display.set_caption("My Game")
	clock = pygame.time.Clock()

	pygame.joystick.init()

def StartStream(): #starts the stream
	print("\n  Starting")

	time.sleep(.5)
	os.system('sudo /home/pi/Henry/VisionRobot/Testing/apache/start.sh' + " &") #calls the start function
	time.sleep(.5)
	
	print("\n  Stream started")
	
	stream_on=True
	pause=True	

def StopStream(): #stops the stream
	print("\n  Stopping")

	time.sleep(.5)	
	os.system('sudo /home/pi/Henry/VisionRobot/Testing/apache/stop.sh' + " &") #calls the stop script
	time.sleep(.5)

	print("\n  Stream stopped")
	
	stream_on=False
	pause=False

def PauseStream(): #runs the stop script, takes a picture, and restarts the stream
	print("\n  Pausing")
	time.sleep(.5)
	os.system('sudo /home/pi/Henry/VisionRobot/Testing/apache/stop.sh' + " &")
	print("\n  Stream paused")
	time.sleep(.5)

	take_photo()

	time.sleep(.5)

	print("\n  Stream restarting")
	time.sleep(.5)
	os.system('sudo /home/pi/Henry/VisionRobot/Testing/apache/start.sh' + " &")
	time.sleep(.5)
	print("\n  Stream on")				

done = False
current_pos=90
stream_on = False
pause = False

PygameSetup()#starts pygame
StopStream()#makes sure the stream is off at start
print_ps4Menu()#prints the menu
set_servo() #puts the servo at its starting location



while done==False: #the while loop for the whole thing
        for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                   	done=True # Flag that we are done so we exit this loop
        joystick_count = pygame.joystick.get_count()
        for i in range(joystick_count):
               	joystick = pygame.joystick.Joystick(i)
                joystick.init()

	button3 = joystick.get_button(3)
       
	if joystick.get_axis(1)==-1: #forward
		fwd()
	elif joystick.get_axis(0)==-1: #left
                left()
        elif joystick.get_axis(1)>=.8: #backward
                bwd()
        elif joystick.get_axis(0)>=.8: #right
                right()
        else:
                stop()
                
	if joystick.get_button(7)==True: #speeds it up
		increase_speed()
	elif joystick.get_button(6)==True: #slows it down
		decrease_speed()
	
	if joystick.get_button(11)==True: # sets the servo at 90
		current_pos = 90
		servo(current_pos)
		time.sleep(.1)
		disable_servo()
		print(current_pos)	

	if joystick.get_axis(5)==-1: #adjusts the servo up 5 degrees
		current_pos += 5
		servo(current_pos)
		time.sleep(.1)
		disable_servo()
		print(current_pos)

	elif joystick.get_axis(5)>=.8: #adjusts the servo down 5 degrees
		current_pos -= 5
		servo(current_pos)
		time.sleep(.1)
		disable_servo()
		print(current_pos)
		
	if joystick.get_button(4)==True:
		left_rot()
	
	if joystick.get_button(5)==True:
		right_rot()

	if joystick.get_button(0)==True: #button takes a photo
		take_photo()

	if joystick.get_button(1)==True and stream_on==False: #button starts the stream
		StartStream()
	
	if joystick.get_button(2)==True and stream_on==True: #button stops the stream
		StopStream()	
	
	if button3==True and pause==True: #runs the stop-picture-start script
		PauseStream()		
	
	if current_pos in range(170,185): #keeps the servo from going over 180 degrees
		if current_pos >=180:
			current_pos -= 5
			servo(current_pos)
			time.sleep(.1)
			disable_servo()
	if current_pos in range(0,5): #keeps the servo from going under 0 degrees
		if current_pos <=0:
			current_pos += 5
			servo(current_pos)
			time.sleep(.1)
			disable_servo()
