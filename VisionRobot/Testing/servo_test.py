from __future__ import print_function
from __future__ import division
from builtins import input

from gopigo import *
import time
import sys
import atexit
atexit.register(stop)

def print_menu():
	print
	print("  CONTROLS")
	print
	print("  Press 's' to reset to home")
	print("  Press 'd' to set to specific location")
	print("  Press '?' to print menu")
print_menu()
while True:
	print("\nCmd:",end="")
	inp=input()
	if inp=='s':
		servo(90)
		time.sleep(.1)
	elif inp=='d':
		print("Enter location:",end="")
		servo(int(input()))
		time.sleep(.1)
	elif inp=='?':
		print_menu()	
	time.sleep(.1)
	disable_servo()
