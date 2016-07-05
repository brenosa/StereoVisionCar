from dronekit import connect, VehicleMode
import time

connection_string = "/dev/ttyUSB0";

# Connect to the Vehicle
print 'Connecting to vehicle on: %s' % connection_string
vehicle = connect(connection_string, baud=921600, wait_ready=True)

print "Param: %s" % vehicle.parameters['ARMING_CHECK']

def arm():
    """
    Arms vehicle
    """

    print "Basic pre-arm checks"
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print " Waiting for vehicle to initialise..."
        time.sleep(1)
        
    print "Arming motors"   
    vehicle.mode = VehicleMode("HOLD")
    vehicle.armed = True    

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:      
        print " Waiting for arming..."
        time.sleep(1)   

arm()

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


print "Setting to MANUAL"   
vehicle.mode = VehicleMode("MANUAL")

# Override channels
print "\nChannel overrides: %s" % vehicle.channels.overrides

print "Set Ch2 override to 200 (indexing syntax)"
vehicle.channels.overrides['2'] = 1200
print " Channel overrides: %s" % vehicle.channels.overrides
print " Ch2 override: %s" % vehicle.channels.overrides['2']

time.sleep(5)  

# Clear override by setting channels to None
print "\nCancel Ch2 override (indexing syntax)"
vehicle.channels.overrides['2'] = None
print " Channel overrides: %s" % vehicle.channels.overrides 


#Close vehicle object before exiting script
print "\nClose vehicle object"
vehicle.close()

print("Completed")
