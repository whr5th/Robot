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
def print_menu():
	print
	print("  Controls")
	print
	print("  Type 'w' to go forward")
	print("  Type 'a' to turn left")
	print("  Type 'd' to turn right")
	print("  Type 's' to go backwards")
	print("  Type 'x' to stop")
	print("  Type 'i' to increase speed")
	print("  Type 'o' to decrease speed")
	print("  Type 'p' to adjust trim")
	print("  Type 'f' to set servo position")
	print("  Type 'g' to set servo back home")
	print("  Type '?' to reprint menu")

def print_ps4Menu():
	print
	print("  Controls")
	print
	print("  Left Joystick to dive motors")
	print("  Right Joystick to control servo")
	print("  Press square to take photo")
	
def take_photo():
	camera = picamera.PiCamera()
	camera.capture('image.jpg')
	camera.close()
	print("\n    You just took a photo")

def set_servo():
	servo(90)
	time.sleep(.1)
	disable_servo()
	print("90")

def PygameSetup():
	pygame.init()
	size = [500, 700]
	screen = pygame.display.set_mode(size)

	pygame.display.set_caption("My Game")
	clock = pygame.time.Clock()

	pygame.joystick.init()

def StartStream():
	print("\n  Starting")

	time.sleep(.5)
	os.system('sudo /home/pi/Henry/VisionRobot/Testing/apache/start.sh' + " &")
	time.sleep(.5)
	
	print("\n  Stream started")
	
	stream_on=True
	pause=True	

def StopStream():
	print("\n  Stopping")

	time.sleep(.5)	
	os.system('sudo /home/pi/Henry/VisionRobot/Testing/apache/stop.sh' + " &")
	time.sleep(.5)

	print("\n  Stream stopped")
	
	stream_on=False
	pause=False


def PauseStream():
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

PygameSetup()
StopStream()
print_ps4Menu()
set_servo()



while done==False:
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
	elif joystick.get_axis(0)==-1:
                left()
        elif joystick.get_axis(1)>=.8:
                bwd()
        elif joystick.get_axis(0)>=.8:
                right()
        else:
                stop()
                
	if joystick.get_button(7)==True:
		increase_speed()
	elif joystick.get_button(6)==True:
		decrease_speed()
	
	if joystick.get_button(11)==True:
		current_pos = 90
		servo(current_pos)
		time.sleep(.1)
		disable_servo()
		print(current_pos)	

	if joystick.get_axis(5)==-1:
		current_pos += 5
		servo(current_pos)
		time.sleep(.1)
		disable_servo()
		print(current_pos)

	elif joystick.get_axis(5)>=.8:
		current_pos -= 5
		servo(current_pos)
		time.sleep(.1)
		disable_servo()
		print(current_pos)
		
	if joystick.get_button(4)==True:
		left_rot()
	
	if joystick.get_button(5)==True:
		right_rot()

	if joystick.get_button(0)==True:
		take_photo()

	if joystick.get_button(1)==True and stream_on==False:
		StartStream()
	
	if joystick.get_button(2)==True and stream_on==True:
		StopStream()	
	
	if button3==True and pause==True:
		PauseStream()		
	
	if current_pos in range(170,185):
		if current_pos >=180:
			current_pos -= 5
			servo(current_pos)
			time.sleep(.1)
			disable_servo()
	if current_pos in range(0,5):
		if current_pos <=0:
			current_pos += 5
			servo(current_pos)
			time.sleep(.1)
			disable_servo()
