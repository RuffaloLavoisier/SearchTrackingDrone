# multiprocessing without gpio but serial com
# USAGE
# python pan_tilt_tracking.py --cascade haarcascade_frontalface_default.xml

# import necessary packages
from multiprocessing import Manager
from multiprocessing import Process
from imutils.video import VideoStream
from pyimagesearch.objcenter import ObjCenter
from pyimagesearch.pid import PID
#import pantilthat as pth
import argparse
import signal
import time
import sys
import cv2
import RPi.GPIO as GPIO
import serial
# define the range for the motors
servoRange = (-90, 90)
ser = serial.Serial('/dev/ttyUSB0',9600)

# function to handle keyboard interrupt
def signal_handler(sig, frame):
	# print a status message
	print("[INFO] You pressed `ctrl + c`! Exiting...")

	# disable the servos
#	pth.servo_enable(1, False)
#	pth.servo_enable(2, False)

	# exit
	sys.exit()

def obj_center(args, objX, objY, centerX, centerY):
	# signal trap to handle keyboard interrupt
	signal.signal(signal.SIGINT, signal_handler)

	# start the video stream and wait for the camera to warm up
	vs = VideoStream(src=-1).start()
	time.sleep(2.0)

	# initialize the object center finder
	obj = ObjCenter(args["cascade"])

	# loop indefinitely
	while True:
		# grab the frame from the threaded video stream and flip it
		# vertically (since our camera was upside down)
		frame = vs.read()
		frame = cv2.flip(cv2.flip(frame, 1),0)

		# calculate the center of the frame as this is where we will
		# try to keep the object
		(H, W) = frame.shape[:2]
		centerX.value = W // 2
		centerY.value = H // 2

		# find the object's location
		objectLoc = obj.update(frame, (centerX.value, centerY.value))
		((objX.value, objY.value), rect) = objectLoc

		# extract the bounding box and draw it
		if rect is not None:
			(x, y, w, h) = rect
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0),
				2)

		# display the frame to the screen
		cv2.imshow("Pan-Tilt Face Tracking", frame)
		cv2.waitKey(1)

def pid_process(output, p, i, d, objCoord, centerCoord):
	# signal trap to handle keyboard interrupt
	signal.signal(signal.SIGINT, signal_handler)

	# create a PID and initialize it
	p = PID(p.value, i.value, d.value)
	p.initialize()

	# loop indefinitely
	while True:
		# calculate the error
		error = centerCoord.value - objCoord.value

		# update the value
		output.value = p.update(error)
def map(x,input_min,input_max,output_min,output_max):
	return (x-input_min)*(output_max-output_min)/(input_max-input_min)+output_min

def in_range(val, start, end):
	# determine the input vale is in the supplied range
	return (val >= start and val <= end)

def set_servos(pan, tlt):
	# signal trap to handle keyboard interrupt
	signal.signal(signal.SIGINT, signal_handler)

	# loop indefinitely
	while True:
		# the pan and tilt angles are reversed
		panAngle = -1 * pan.value
		tltAngle = -1 * tlt.value

		# if the pan angle is within the range, pan
		if in_range(panAngle, servoRange[0], servoRange[1]):
		# we want serial com but map func use in arduino
#			pan_filter = map(panAngle,-90,90,1,180) # output,ip min ,ip max ,op min ,op max
			pan_filter = panAngle
		# if the tilt angle is within the range, tilt
		if in_range(tltAngle, servoRange[0], servoRange[1]):
			tilt_filter = tltAngle
#----------------------------------------------------
		if tltAngle < 0 and panAngle < 0: # all -
			separated = 0
		elif tltAngle >= 0 and panAngle >= 0: # all +
			separated = 3
		elif tltAngle < 0 and panAngle >= 0: # two -
			separated = 2
		elif tltAngle >= 0 and panAngle < 0: # one -	
			separated = 1

		tilt_filter =  abs(tilt_filter)
		pan_filter = abs(pan_filter)
		print (str(panAngle)+" / "+str(pan_filter)+" / "+str(tltAngle)+" / "+str(tilt_filter)+" / "+str(separated))
		mix_value = int(pan_filter)*1000 + int(tilt_filter)*10 + int(separated)
		
#		mix_value = str(int(pan_filter))+" / "  +str(int(tilt_filter))+" / "+str(int(separated))
		print ("int mix value : " + str(mix_value) )
		mix_value = mix_value * 0.1 # now change
		print ("before mix value : "+ str(mix_value))
		str_mix_value = str(mix_value)
		number_box = str_mix_value.split(".")
		if len(number_box[0]) == 4:
			mix_value = str_mix_value[:6]
		elif len(number_box[0]) == 3:
			mix_value = str_mix_value[:5]

		print ("after mix value : " + str(mix_value))
		#read_check = ser.readline()
		#f_r_c = read_check.decode()[:2]
		#print "check val : " + str(f_r_c)
		ser.write(str(mix_value).encode("utf-8"))
		read = ser.readline()
#		read = read.decode()[:2]
		print (str(read))

# check to see if this is the main body of execution
if __name__ == "__main__":
	# construct the argument parser and parse the arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-c", "--cascade", type=str, required=True,
		help="path to input Haar cascade for face detection")
	args = vars(ap.parse_args())

	# start a manager for managing process-safe variables
	with Manager() as manager:
		# enable the servos
#		pth.servo_enable(1, True)
#		pth.servo_enable(2, True)

		# set integer values for the object center (x, y)-coordinates
		centerX = manager.Value("i", 0)
		centerY = manager.Value("i", 0)

		# set integer values for the object's (x, y)-coordinates
		objX = manager.Value("i", 0)
		objY = manager.Value("i", 0)

		# pan and tilt values will be managed by independed PIDs
		pan = manager.Value("i", 0)
		tlt = manager.Value("i", 0)

		# set PID values for panning
		panP = manager.Value("f", 0.09)
		panI = manager.Value("f", 0.08)
		panD = manager.Value("f", 0.002)

		# set PID values for tilting
		tiltP = manager.Value("f", 0.11)
		tiltI = manager.Value("f", 0.10)
		tiltD = manager.Value("f", 0.002)

		# we have 4 independent processes
		# 1. objectCenter  - finds/localizes the object
		# 2. panning       - PID control loop determines panning angle
		# 3. tilting       - PID control loop determines tilting angle
		# 4. setServos     - drives the servos to proper angles based
		#                    on PID feedback to keep object in center
		processObjectCenter = Process(target=obj_center,
			args=(args, objX, objY, centerX, centerY))
		processPanning = Process(target=pid_process,
			args=(pan, panP, panI, panD, objX, centerX))
		processTilting = Process(target=pid_process,
			args=(tlt, tiltP, tiltI, tiltD, objY, centerY))
		processSetServos = Process(target=set_servos, args=(pan, tlt))

		# start all 4 processes
		processObjectCenter.start()
		processPanning.start()
		processTilting.start()
		processSetServos.start()

		# join all 4 processes
		processObjectCenter.join()
		processPanning.join()
		processTilting.join()
		processSetServos.join()

		# disable the servos
#		pth.servo_enable(1, False)
#		pth.servo_enable(2, False)
