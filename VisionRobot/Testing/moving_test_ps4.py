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

#print_menu() #prints the menu at the start of the program

pygame.init()
# Set the width and height of the screen [width,height]
size = [500, 700]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("My Game")
#Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Initialize the joysticks
pygame.joystick.init()
current_pos=90

while done==False:
        for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    done=True # Flag that we are done so we exit this loop
        joystick_count = pygame.joystick.get_count()
        for i in range(joystick_count):
                joystick = pygame.joystick.Joystick(i)
                joystick.init()
        
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
		servo(90)
		time.sleep(.1)
		disable_servo()
	
	if joystick.get_axis(5)==-1:
		current_pos += 5
		servo(current_pos)
		time.sleep(.1)
		disable_servo()
	elif joystick.get_axis(5)>=.8:
		current_pos -= 5
		servo(current_pos)
		time.sleep(.1)
		disable_servo()
