import RPi.GPIO as GPIO

def funz(param):

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.OUT)
    GPIO.output(17, param)
