from picamera import PiCamera
from time import sleep

camera = PiCamera()

camera.capture('./www/images/image.jpg')
print("Catch finished ")