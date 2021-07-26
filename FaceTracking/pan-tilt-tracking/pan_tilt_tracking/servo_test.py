import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) # use phy pin

pan_pin = 40
#tilt_pin = 37 # not yet

GPIO.setup(pan_pin, GPIO.OUT)
#GPIO.setup(tilt_pin, GPIO.OUT)

freq = 50

pwm_pan = GPIO.PWM(pan_pin, freq) # pin and freq
#pwm_tilt = GPIO.PWM(tilt_pin, freq)

pwm_pan.start(0)
#pwm_tilt.start(0)


while True:
	pwm_pan.ChangeDutyCycle(3)
	time.sleep(1)
	
	pwm_pan.ChangeDutyCycle(7)
	time.sleep(1)
	
	pwm_pan.ChangeDutyCycle(12)
	time.sleep(1)

