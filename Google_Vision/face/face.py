"""
Google Vision API Tutorial with a Raspberry Pi and Raspberry Pi Camera.  See more about it here:  https://www.dexterindustries.com/howto/use-google-cloud-vision-on-the-raspberry-pi/

Use Google Cloud Vision on the Raspberry Pi to take a picture with the Raspberry Pi Camera and classify it with the Google Cloud Vision API.   First, we'll walk you through setting up the Google Cloud Platform.  Next, we will use the Raspberry Pi Camera to take a picture of an object, and then use the Raspberry Pi to upload the picture taken to Google Cloud.  We can analyze the picture and return labels (what's going on in the picture), logos (company logos that are in the picture) and faces.

This script uses the Vision API's label detection capabilities to find a label
based on an image's content.


Henry Roberts
SM Info Engineering
Google Vision APi Code
"""

import argparse		#unaltered code from the source
import base64
import picamera		#imports the commands for the camera
import json		#imports the json commands
import os		#imports the system commands
import time		#imports delay commands

from gtts import gTTS		#google text to speech api
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

def takephoto():				#the raspberry pi takes a photo from the PiCamera
    camera = picamera.PiCamera()
    camera.capture('face.jpg') 			#saves the picture as 'face.jpg'

def main():
    takephoto() # First take a picture
    """Run a label request on a single image"""

    credentials = GoogleCredentials.get_application_default()		#finds the exported google application credentials
    service = discovery.build('vision', 'v1', credentials=credentials)

    with open('face.jpg', 'rb') as image:			#opens 'face.jpg' 
        image_content = base64.b64encode(image.read())		#encodes the image using base64 so that google can read it
        service_request = service.images().annotate(body={ 	#declares what JSON data is wanted back
            'requests': [{
                'image': {
                    'content': image_content.decode('UTF-8')
                },
                'features': [{
                    'type': 'FACE_DETECTION',			#declares that it wants the facial detection software 
                    'maxResults': 10				#lists the maximum results 
                }]
            }]
        })
        response = service_request.execute()		#executes the json request
		
	#end of source code

	#my code startes here	
	parse_response(response)

def parse_response(response):

	face_response = json.dumps(response, indent=4, sort_keys=True) 			#the command json.dumps converts the json data into a string 		
	analysis = json.loads(face_response)['responses'][0]['faceAnnotations'][0]	#the json.loads command reads the new string of data. then the headers are delcared to specify what data is wanted 

	anger_raw = analysis['angerLikelihood']		#finding and storing the anger variable
	happy_raw = analysis['joyLikelihood']		#finding and storing the happy variable
	sorrow_raw = analysis['sorrowLikelihood']	#finding and storing the sorrow variable
	surprise_raw = analysis['surpriseLikelihood']	#finding and storing the surprise variable
	
	#each emotion has five different possible outcomes 
	#VERY_UNLIKELY, UNLIKELY, POSSIBLE, LIKELY, VERY_LIKELY

	#each of these 'if' statements changes the words associated with each outcome 

	if anger_raw == 'VERY_UNLIKELY':		
		anger = 'You do not look angry.'
	if anger_raw == 'UNLIKELY':
		anger = 'It is unlikely that you are angry.'
	if anger_raw == 'POSSIBLE':
		anger = 'You might be angry.'
	if anger_raw == 'LIKELY':
		anger = 'It is likely that you are angry.'
	if anger_raw == 'VERY_LIKELY':
		anger = 'You look  angry.'

	if happy_raw == 'VERY_UNLIKELY':
		happy = 'You do not look happy.'
	if happy_raw == 'UNLIKELY':
		happy = 'It is unlikely that you are happy.'
	if happy_raw == 'POSSIBLE':
		happy = 'You might be happy.'
	if happy_raw == 'LIKELY':
		happy = 'It is likely that you are happy.'
	if happy_raw == 'VERY_LIKELY':
		happy = 'You look happy.'

	if sorrow_raw == 'VERY_UNLIKELY':
		sorrow = 'You do not look sad.'
	if sorrow_raw == 'UNLIKELY':
		sorrow = 'It is unlikely that you are sad.'
	if sorrow_raw == 'POSSIBLE':
		sorrow = 'You might be sad.'
	if sorrow_raw == 'LIKELY':
		sorrow = 'It is likely that you are sad.'
	if sorrow_raw == 'VERY_LIKELY':
		sorrow = 'You look sad.'

	if surprise_raw == 'VERY_UNLIKELY':
		surprise = 'You do not look surprised.'
	if surprise_raw == 'UNLIKELY':
		surprise = 'It is unlikely that you are surprised.'
	if surprise_raw == 'POSSIBLE':
		surprise = 'You might be surprised.'
	if surprise_raw == 'LIKELY':
		surprise = 'It is likely that you are surprised.'
	if surprise_raw == 'VERY_LIKELY':
		surprise = 'You look surprised.'

	#lots of blank 'print' commands to make the terminal output look cleaner
	#added delays to make terminal look cleaner

	print
	print	
	print("Welcome! We are reading your emotions now.")	#first thing the terminal prints
	print
	print	
	time.sleep(2)
	print(anger)	#prints the words associated with the anger variable from this specific outcome
	print
	time.sleep(1)
	print(happy)	#prints the words associated with the happy variable from this specific outcome
	print
	time.sleep(1)	
	print(sorrow)	#prints the words associated with the sorrow variable from this specific outcome
	print
	time.sleep(1)
	print(surprise)	#prints the words associated with the surprise variable from this specific outcome
	print
	print
	print("Have a good day!")	#prints the closing statement
	print("_________________________________")
	print

	#google Text To Speach APi
		
	tts_answer = gTTS("Welcome! We are reading your emotions now." + anger + happy + sorrow + surprise + "Have a good day!", lang='en')
		#declares what the gTTS is supposed to read

	tts_answer.save('face.mp3')
		#saves the gTTS as an mp3 file
	
	os.system('mpg321 face.mp3')
		#plays the mp3 file	

	with open("face.json", "w") as face_data:	#creates a new file names 'face.json'/overwrites the current 'face.json' file and opens it as write file
		json.dump(response, face_data)		#stores the original json data from google vision APi as a back up

	#my code ends
		
#runs the main program
if __name__ == '__main__':

    main()
