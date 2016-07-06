from dronekit import connect, VehicleMode
import time


def connect(connection_string):		 
	# Connect to the Vehicle
	print 'Connecting to vehicle on: %s' % connection_string
	vehicle = connect(connection_string, baud=921600, wait_ready=True)
	print 'Connected!'


def goTo(direction , orientation, speed):
	# Override channels
	print "\nChannel overrides: %s" % vehicle.channels.overrides

	print "Set Ch2 override to 200 (indexing syntax)"
	vehicle.channels.overrides['2'] = 1200
	print " Channel overrides: %s" % vehicle.channels.overrides
	print " Ch2 override: %s" % vehicle.channels.overrides['2']


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
#
goTo(direction , orientation, speed) 
#
time.sleep(5)
#
changeMode("HOLD")
#
disarm()
#
disconnect()

#TODO create module/compass

