import RPi.GPIO as GPIO

class Led(object):

	def __init__(self):
		self.led = 20
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.led, GPIO.OUT)
		
	def turnOnLed(self):
		GPIO.output(self.led, True)
		
	def turnOffLed(self):
		GPIO.output(self.led, False)
