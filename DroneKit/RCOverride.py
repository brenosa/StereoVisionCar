from dronekit import connect, VehicleMode
from pymavlink import mavutil
from threading import Thread
from twisted.internet import reactor
from sysfs.gpio import Controller, OUTPUT, INPUT, RISING
import time

vehicle = 0


#
#CHANGE SYSID_GSC PARAMETER TO 255 FIRST!
#

def distanceSensor():

	Controller.available_pins = [23, 24]

	TRIG =  Controller.alloc_pin(23, OUTPUT)
	ECHO = Controller.alloc_pin(24, INPUT)

	print "Distance Measurement In Progress"

	while True:  
		TRIG.reset()
		time.sleep(2)
		TRIG.set()
		time.sleep(0.00001)
		TRIG.reset()
		while ECHO.read()==0:
			pulse_start = time.time()
		while ECHO.read()==1:
			pulse_end = time.time()
		pulse_duration = pulse_end - pulse_start
		distance = pulse_duration * 17150
		distance = round(distance, 2)
		print "Distance:",distance,"cm"
		if distance <= 60:
			#STOP
			manualControl('NONE', 0, 'NONE', 0)			
			print "HOLD",distance,"cm"
		else:				
			#FORWARD
			manualControl('FORWARD', 20, 'NONE', 0)		
	GPIO.cleanup()

def manualControl(throttle , speed, steering, steer_intensity):
	global vehicle	
	#Set channels
	throttle_channel = 1	
	steer_channel = 3	
	
	#Normalize speed	
	if speed >= 0 and speed <=100:	
		speed = speed * 5
	else:
		print 'Speed out of range (0~100).'
		return

	#Set throttle
	if throttle == 'FORWARD':
		throttle = 1500 + speed
	elif throttle == 'BACKWARD':
		throttle = 1500 - speed
	elif throttle == 'NONE':
		throttle = 1500	
	else:
		print 'Unknown throttle. Use \'FORWARD\', \'BACKWARD\' or \'NONE\').'
		return		

	#Normalize turn intensity	
	if steer_intensity >= 0 and steer_intensity <=100:
		steer_intensity = steer_intensity * 5
	else:
		print 'Turn intensity out of range (0~100).'
		return
		
	#Set steering
	if steering == 'RIGHT':
		steering = 1500 + steer_intensity
	elif steering == 'LEFT':
		steering = 1500 - steer_intensity
	elif steering == 'NONE':
		steering = 1500
	else:
		print 'Unknown direction. Use \'RIGHT\', \'LEFT\' or \'NONE\').'
		return

	# Override channels
	print "\nChannel overrides: %s" % vehicle.channels.overrides
	#run_time = 0
	#while run_time < 5:
	#time.sleep(1)
	#Set throttle
	vehicle.channels.overrides[throttle_channel] = throttle

	#Set steering
	vehicle.channels.overrides[steer_channel] = steering
	
	#vehicle.channels.overrides[throttle_channel] = None
	#vehicle.channels.overrides[steer_channel] = None
	
	#Debug
	print " Channel overrides: %s" % vehicle.channels.overrides
	
def connectVehicle(connection_string):
	global vehicle		 
	# Connect to the Vehicle
	print 'Connecting to vehicle on: %s' % connection_string
	vehicle = connect(connection_string, wait_ready=True, baud=921600)
	print 'Connected!'

def disconnectVehicle():
	global vehicle	
	#Close vehicle object before exiting script	
	vehicle.close()
	print "Vehicle object closed"
	
def changeMode(mode):	
	global vehicle	
	vehicle.mode = VehicleMode(mode)
	while vehicle.mode != mode:
		pass
		#Debug
		#print "Setting to " + mode
		
	print 'Mode changed!'	
	
def disarm():
	global vehicle	
	vehicle.armed = False
	while vehicle.armed:      
        	print " Waiting for disarming..."
        	time.sleep(1)
	print "Vehicle disarmed" 

def arm():
	global vehicle	
	print "Basic pre-arm checks"
	# Don't try to arm until autopilot is ready
	#while not vehicle.is_armable:
		#print " Waiting for vehicle to initialise..."
		#time.sleep(1)
	
	print "Arming motors"   	
	vehicle.armed = True    

	# Confirm vehicle armed before attempting to take off
	while not vehicle.armed:      
		print " Waiting for arming..."
		time.sleep(1)
		

def status():
	global vehicle	
	# vehicle is an instance of the Vehicle class
	print "Autopilot Firmware version: %s" % vehicle.version
	print "Autopilot capabilities (supports ftp): %s" % vehicle.capabilities.ftp
	print "Global Location: %s" % vehicle.location.global_frame
	print "Global Location (relative altitude): %s" % vehicle.location.global_relative_frame
	print "Local Location: %s" % vehicle.location.local_frame    #NED
	print "Attitude: %s" % vehicle.attitude
	print "Velocity: %s" % vehicle.velocity
	print "GPS: %s" % vehicle.gps_0
	print "Groundspeed: %s" % vehicle.groundspeed
	print "Airspeed: %s" % vehicle.airspeed
	print "Gimbal status: %s" % vehicle.gimbal
	print "Battery: %s" % vehicle.battery
	print "EKF OK?: %s" % vehicle.ekf_ok
	print "Last Heartbeat: %s" % vehicle.last_heartbeat
	print "Rangefinder: %s" % vehicle.rangefinder
	print "Rangefinder distance: %s" % vehicle.rangefinder.distance
	print "Rangefinder voltage: %s" % vehicle.rangefinder.voltage
	print "Heading: %s" % vehicle.heading
	print "Is Armable?: %s" % vehicle.is_armable
	print "System status: %s" % vehicle.system_status.state
	print "Mode: %s" % vehicle.mode.name    # settable
	print "Armed: %s" % vehicle.armed    # settable   

#
connectVehicle('/dev/ttyUSB0')

#
#status()

vehicle.parameters['FS_THR_ENABLE']=1
vehicle.parameters['FS_THR_VALUE']=1
vehicle.parameters['FS_TIMEOUT']=100
vehicle.parameters['FS_ACTION']=0
vehicle.parameters['FS_GCS_ENABLE']=0


#
arm()
#
changeMode('MANUAL')

#
#t = Thread(target=distanceSensor)
#t.start()

#
distanceSensor()


	#*****************************************Commands examples*********************************************#
									#FORWARD
									#manualControl('FORWARD', 20, 'NONE', 0)

									#FOWARD RIGHT
									#manualControl('FORWARD', 50, 'RIGHT', 50)

									#STOP
									#manualControl('NONE', 0, 'NONE', #0)

									#SPIN LEFT
									#manualControl('NONE', 0, 'LEFT', 30)

									#BACKWARD
									#manualControl('BACKWARD', 20, 'NONE', 0)

									#BACKWARD RIGHT
									#manualControl('BACKWARD', 50, 'RIGHT', 50)

	#********************************************************************************************************#

#
changeMode('HOLD')

#
disarm()

#
disconnectVehicle()

#TODO create module/compass
