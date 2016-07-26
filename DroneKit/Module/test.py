import RCOverideAPI

#Connect to Pixhawk in the specified port
RCOverideAPI.connectVehicle('/dev/ttyUSB0')

#Get all available vehicle status
#RCOverideAPI.status()

#CHANGE SYSID_GSC PARAMETER TO 255 BEFORE FIRST USE
#RCOverideAPI.vehicle.parameters['SYSID_GSC']=255

#MAKE SURE FS_THR_ENABLE IS ENABLED
#RCOverideAPI.vehicle.parameters['FS_THR_ENABLE']=1

#Start automatic mode, avoiding obstacles
RCOverideAPI.distanceSensor()


	#*****************************************Manual commands examples*********************************************#
									#FORWARD
									#RCOverideAPI.manualControl('FORWARD', 20, 'NONE', 0)

									#FOWARD RIGHT
									#RCOverideAPI.manualControl('FORWARD', 50, 'RIGHT', 50)

									#STOP
									#RCOverideAPI.manualControl('NONE', 0, 'NONE', 0)

									#SPIN LEFT
									#RCOverideAPI.manualControl('NONE', 0, 'LEFT', 30)

									#BACKWARD
									#RCOverideAPI.manualControl('BACKWARD', 20, 'NONE', 0)

									#BACKWARD RIGHT
									#RCOverideAPI.manualControl('BACKWARD', 50, 'RIGHT', 50)

	#********************************************************************************************************#

#Set mode to HOLD after use
RCOverideAPI.changeMode('HOLD')

#Disarm vehicle after use
RCOverideAPI.disarm()

#Disconnect from Pixhawk
RCOverideAPI.disconnectVehicle()
