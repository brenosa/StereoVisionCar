from dronekit import connect, VehicleMode
from pymavlink import mavutil
import time

vehicle = 0

def connectVehicle(connection_string):
	global vehicle		 
	# Connect to the Vehicle
	print 'Connecting to vehicle on: %s' % connection_string
	vehicle = connect(connection_string, wait_ready=True, baud=921600)
	print 'Connected!'

#
#CHANGE SYSID_GSC PARAMETER TO 255 FIRST!
#

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

	#Set throttle
	vehicle.channels.overrides[throttle_channel] = throttle

	#Set steering
	vehicle.channels.overrides[steer_channel] = steering

	#Debug
	print " Channel overrides: %s" % vehicle.channels.overrides
	


def changeMode(mode):	
	global vehicle	
	vehicle.mode = VehicleMode(mode)
	while vehicle.mode != mode:
		pass
		#print "Setting to " + mode
		
	print 'Mode changed!'
	
	
def disarm():
	global vehicle	
	vehicle.armed = False
	while vehicle.armed:      
        	print " Waiting for disarming..."
        	time.sleep(1)
	print "Vehicle disarmed" 	

def disconnect():
	global vehicle	
	#Close vehicle object before exiting script	
	vehicle.close()
	print "Vehicle object closed"
	

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

   
def debug():
	global vehicle	
	print "Param: %s" % vehicle.parameters['ARMING_CHECK']

	# Get all original channel values (before override)
	print "Channel values from RC Tx:", vehicle.channels

	# Access channels individually
	print "Read channels individually:"
	print " Ch1: %s" % vehicle.channels['1']
	print " Ch2: %s" % vehicle.channels['2']
	print " Ch3: %s" % vehicle.channels['3']
	print " Ch4: %s" % vehicle.channels['4']
	print " Ch5: %s" % vehicle.channels['5']
	print " Ch6: %s" % vehicle.channels['6']
	print " Ch7: %s" % vehicle.channels['7']
	print " Ch8: %s" % vehicle.channels['8']
	print "Number of channels: %s" % len(vehicle.channels)


#
connectVehicle('/dev/ttyUSB0')

#
#status()

#
arm()

#
changeMode('MANUAL')
#status()

#FORWARD
#manualControl('FORWARD', 50, 'NONE', 0)

#FOWARD RIGHT
#manualControl('FORWARD', 50, 'RIGHT', 50)

#SPIN LEFT
manualControl('NONE', 0, 'LEFT', 50)

#BACKWARD
#manualControl('BACKWARD', 50, 'NONE', 0)

#BACKWARD RIGHT
#manualControl('BACKWARD', 50, 'RIGHT', 50)
#print "\nChannel overrides: %s" % vehicle.channels.overrides
#while True:
#	vehicle.channels.overrides[3] = 1800
#print "\nChannel overrides: %s" % vehicle.channels


#
time.sleep(10)
print 'slept'
#
changeMode('HOLD')
#status()
#
#disarm()

#
disconnect()

#TODO create module/compass/STATUS
