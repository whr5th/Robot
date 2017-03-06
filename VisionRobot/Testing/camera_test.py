import picamera
camera = picamera.PiCamera()
camera.capture('test.jpg')
camera.close()
