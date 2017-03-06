from __future__ import print_function, division #importing the ability to customize the terminal 
from builtins import input

from gopigo import * #imports the gopigo library
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

print_menu() #prints the menu at the start of the program
while True:
	print("\nCmd:",end="") #"\n" is formatting so it formats a new line with the phrase 'Cmd' everytime
	inp=input() #takes the input of what is put into the console 
	if inp=='w': #forward
		fwd()
	elif inp=='a': #left
		left()
	elif inp=='d': #right
		right()
	elif inp=='s': #back
		bwd()
	elif inp=='x': #stop
		stop()
	elif inp=='f':
		print("Enter Servo position:",end="") #new line with new place to input servo position
		servo(int(input())) #the servo is set to what was inputed
		time.sleep(.1) #delay for .1 seconds
		disable_servo() #disables the servo so there is no jitter
	elif inp=='g': # puts the servo back at 90 degrees 
		servo(90)
		time.sleep(.1)
		disable_servo()
	elif inp=='i': #makes it go fasters
		increase_speed() 
	elif inp=='o': #goes slower
		decrease_speed()
	elif inp=='p': #input value of making the motors more powerful
		print(" Enter trim value:",end="")
		trim_write(int(input()))
		time.sleep(.1)
	elif inp=='?':
		print_menu()
