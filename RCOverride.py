from dronekit import connect, VehicleMode
import time


def connect(connection_string):		 
	# Connect to the Vehicle
	print 'Connecting to vehicle on: %s' % connection_string
	vehicle = connect(connection_string, baud=921600, wait_ready=True)
	print 'Connected!'


def manualControl(direction , speed, orientation, turn_intensity):
	#Set channels
	direction_ch = 2	
	orientation_ch = 4	
	
	#Normalize speed	
	if speed >= 0 and speed <=100:	
		speed = speed * 5
	else:
		print 'Speed out of range (0~100).'
		return

	#Set direction
	if direction == 'FORWARD':
		direction = 1500 + speed
	elif direction == 'BACKWARD':
		direction = 1500 - speed
	elif direction == 'NONE':
		direction = 1500	
	else:
		print 'Unknown direction. Use \'FORWARD\', \'BACKWARD\' or \'NONE\').'
		return		

	#Normalize turn intensity	
	if turn_intensity >= 0 and turn_intensity <=100:
		turn_intensity = turn_intensity * 5
	else:
		print 'Turn intensity out of range (0~100).'
		return
		
	#Set orientation
	if orientation == 'RIGHT':
		orientation = 1500 + turn_intensity
	elif orientation == 'LEFT':
		orientation = 1500 - turn_intensity
	elif orientation == 'NONE':
		orientation = 1500
	else:
		print 'Unknown direction. Use \'RIGHT\', \'LEFT\' or \'NONE\').'
		return

	# Override channels
	print "\nChannel overrides: %s" % vehicle.channels.overrides

	#Set direction
	vehicle.channels.overrides[direction_ch] = direction

	#Set orientation
	vehicle.channels.overrides[orientation_ch] = orientation

	#Debug
	print " Channel overrides: %s" % vehicle.channels.overrides
	


def changeMode(mode):	  
	while vehicle.mode != mode:
		print "Setting to " + mode
		vehicle.mode = VehicleMode(mode)
	print 'Mode changed!'
	
	
def disarm():
	vehicle.armed = False
	while vehicle.armed:      
        	print " Waiting for disarming..."
        	time.sleep(1)
	print "Vehicle disarmed" 	

def disconnect():
	#Close vehicle object before exiting script
	
	vehicle.close()
	print "Vehicle object closed"
	
def status():
	print "TODO"

def arm():
	print "Basic pre-arm checks"
    	# Don't try to arm until autopilot is ready
    	while not vehicle.is_armable:
        	print " Waiting for vehicle to initialise..."
        	time.sleep(1)
        
    	print "Arming motors"   	
    	vehicle.armed = True    

    	# Confirm vehicle armed before attempting to take off
    	while not vehicle.armed:      
        	print " Waiting for arming..."
        	time.sleep(1)
   
def debug():
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
connect("/dev/ttyUSB0")

#
arm()

#
changeMode("MANUAL")

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

#
time.sleep(5)

#
changeMode("HOLD")

#
disarm()

#
disconnect()

#TODO create module/compass/STATUS

