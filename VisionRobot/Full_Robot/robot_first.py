#!/usr/bin/env python
from __future__ import print_function
from __future__ import division
from builtins import input

'''
## License
 GoPiGo for the Raspberry Pi: an open source robotics platform for the Raspberry Pi.
 Copyright (C) 2015  Dexter Industries

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/gpl-3.0.txt>.
'''

from gopigo import *
import sys
import atexit
atexit.register(stop)

def print_menu():
	print( "  w	:	Move the GoPiGo forward")
	print( "  a	:	Turn the GoPiGo left")
	print( "  s	:	Move the GoPiGo back")
	print( "  d	:	Turn the GoPiGo right")
	print( "  n	:	Rotate the GoPiGo left in place")
	print( "  m	:	Rotate the GoPiGo right in place")
	print( "  x	:	Stop the GoPiGo")
	print( "  t	:	Increase the speed by 10 (default 200, min:0 max 255)")
	print( "  g	:	Reduce the speed by 10")
	print( "  v	:	Print the voltage of the batteries (should be greater than 10)")
	print( "  st	:	Set servo position")
	print( "  b	:	Run a servo 180 degree sweep")
	print( "  u	:	Get the distance from the ultrasonic ranger")
	print( "  l	:	Turn the LED's on and off")
	print( "  f	:	Print the firmware version on the GoPiGo")
	print( "  tr	:	Read the trim value on the GoPiGo")
	print( "  tw	:	Write the trim value to the GoPiGo")
	print( "  tt	:	Test the trim value to the GoPiGo")
	print( "  ?	:	Print the menu again")
	print( "  z	:	Exit")
	print( "Please type a command and press ENTER: ")
#_______________________
	print
	print( "  1     :       Take Picture")
	print( "  2     :       Run labeling program")
	print( "  3     :       Run emotiion detection")
#_______________________

print( "  ____       ____  _  ____       ")
print( " / ___| ___ |  _ \(_)/ ___| ___  ")
print( "| |  _ / _ \| |_) | | |  _ / _ \ ")
print( "| |_| | (_) |  __/| | |_| | (_) |")
print( " \____|\___/|_|   |_|\____|\___/ ")
print( "")
print( "Welcome to GoPiGo Basic test program\nYou can use this to try out the various features of your GoPiGo\n")
print_menu()
#_________________________________
import argparse
import base64
import picamera
import json

from gtts import gTTS
import os
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

def takephoto():
	camera = picamera.PiCamera()
	camera.capture('/home/pi/Henry/VisionRobot/Full_Robot/google_excess/label.jpg')

def label_main():
	takephoto()

	credentials = GoogleCredentials.get_application_default()
	service = discovery.build('vision', 'v1', credentials=credentials)

	with open('/home/pi/Henry/VisionRobot/Full_Robot/google_excess/label.jpg', 'rb') as image:
                image_content = base64.b64encode(image.read())
                service_request = service.images().annotate(body={
                    'requests': [{
                        'image': {
                            'content': image_content.decode('UTF-8')
                        },
                        'features': [{
                            'type': 'LABEL_DETECTION',
                            'maxResults': 10
                        }]
                    }]
                })
                response = service_request.execute()
                parse_response(response)

        def parse_response(response):
                label = json.dumps(response, indent=4, sort_keys=True)
                items = json.loads(label)['responses'][0]['labelAnnotations']
                
                item = items[0]['description']
                item2 = items[1]['description']
                
                print("We are identifying the item now")
                print
                print
                print
                print("This is likely a " + item)
                print
                print("This is likely a " + item2)	
                print
                print("Have a good day!")
                print("______________________________________________________")
                print
                string = item+ " or a " +item2
                tts = gTTS("Welcome! We are identifying this now.     This is likely a" + string, lang='en')
                tts.save("/home/pi/Henry/VisionRobot/Full_Robot/google_excess/label.mp3")
                os.system("mpg321 /home/pi/Henry/VisionRobot/Full_Robot/google_excess/label.mp3")
                with open("/home/pi/Henry/VisionRobot/Full_Robot/google_excess/label.json", "w") as response2:
                        json.dump(response, response2)
        if __name__ == '__main__':

                main()
#def face_main():



#_______________________________________
while True:
	print( "\nCmd:",end="")
	a=input()
	if a=='w':
		fwd()
	elif a=='a':
		left()
	elif a=='d':
		right()
	elif a=='s':
		bwd()
	elif a=='x':
		stop()
	elif a=='t':
		increase_speed()
	elif a=='g':
		decrease_speed()
	elif a=='v':
		print( "{}V".format(volt()))
	elif a=='b': #servo test
		for i in range(180):
			servo(i)
			print(i)
			time.sleep(.02)
			disable_servo()
	elif a=='z':
		sys.exit()
	elif a=='u':
		print( '{}cm'.format(us_dist(15)))
	elif a=='l':
		led_on(0)
		led_on(1)
		time.sleep(1)
		led_off(0)
		led_off(1)
	elif a=='i':
		motor_fwd()
	elif a=='k':
		motor_bwd()
	elif a=='n':
		left_rot()
	elif a=='m':
		right_rot()
	elif a=='y':
		enc_tgt(1,1,18)
	elif a=='f':
		print( "v{}".format(fw_ver()))
	elif a=='tr':
		val=trim_read()
		if val==-3:
			print( "-3, Trim Value Not set")
		else:
			print( val-100)
	elif a=='tw':
		print( "Enter trim value to write to EEPROM(-100 to 100):",end="")
		val=int(input())
		trim_write(val)
		time.sleep(.1)
		print( "Value in EEPROM: {}".format(trim_read()-100))
	elif a=='tt':
		print( "Enter trim value to test(-100 to 100):",end="")
		val=int(input())
		trim_test(val)
		time.sleep(.1)
		print( "Value in EEPROM: {}".format(trim_read()-100))
	elif a=='st':
		print( "Enter Servo position:",end="")
		val=int(input())
		enable_servo()
		servo(val)
		time.sleep(.1)
	elif a=='?':
		print_menu()
	elif a=='1':
		takephoto()
	elif a=='2':
		label_main()	
	elif a=='3':
		face_main()
	time.sleep(.1)
