"""
Google Vision API Tutorial with a Raspberry Pi and Raspberry Pi Camera.  See more about it here:  https://www.dexterindustries.com/howto/use-google-cloud-vision-on-the-raspberry-pi/

Use Google Cloud Vision on the Raspberry Pi to take a picture with the Raspberry Pi Camera and classify it with the Google Cloud Vision API.   First, we'll walk you through setting up the Google Cloud Platform.  Next, we will use the Raspberry Pi Camera to take a picture of an object, and then use the Raspberry Pi to upload the picture taken to Google Cloud.  We can analyze the picture and return labels (what's going on in the picture), logos (company logos that are in the picture) and faces.

This script uses the Vision API's label detection capabilities to find a label
based on an image's content.

"""

import argparse
import base64
import picamera
import json

from pprint import pprint
from gtts import gTTS
import os
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

def takephoto():
    camera = picamera.PiCamera()
    camera.capture('label.jpg')

def main():
    takephoto() # First take a picture
    """Run a label request on a single image"""

    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('vision', 'v1', credentials=credentials)

    with open('label.jpg', 'rb') as image:
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
	
	print("Welcome! We are identifying the item now")
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
	tts.save("label.mp3")
	os.system("mpg321 label.mp3")
	with open("label.json", "w") as response2:
		json.dump(response, response2)
if __name__ == '__main__':

	main()
