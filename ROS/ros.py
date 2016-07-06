#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
import time
from mavros_msgs.msg import OverrideRCIn
from mavros_msgs.srv import SetMode

#
#CHANGE SYSID_GSC PARAMETER TO 1 FIRST!
#

def manualControl(throttle , speed, steering, steer_intensity):
	pub = rospy.Publisher('mavros/rc/override', OverrideRCIn, queue_size=10)
	rospy.init_node('custom_talker', anonymous=True)
	r = rospy.Rate(10) #10hz
	msg = OverrideRCIn()
		
	#Set channels
	throttle_channel = 1	
	steer_channel = 3	
	
	#Normalize speed	
	if speed >= 0 and speed <=100:	
		speed = speed * 5
	else:
		print 'Speed out of range (0~100).'
		return

	#Set direction
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
	
	#Set throttle
	msg.channels[throttle_channel] = throttle

	#Set orientation
	msg.channels[steer_channel] = steering

	rospy.loginfo(msg)
	pub.publish(msg)
	r.sleep()
	
def changeMode(mode):
	rospy.wait_for_service('/mavros/set_mode')
	change_mode = rospy.ServiceProxy('/mavros/set_mode', SetMode)
	change_mode(custom_mode=mode)

	

def talker():
	pub = rospy.Publisher('mavros/rc/override', OverrideRCIn, queue_size=10)
	r = rospy.Rate(10) #10hz
	msg = OverrideRCIn()
	start = time.time()
	speed='SLOW'
	exec_time=2
	flag=True #time flag
	if speed =='SLOW':
		msg.channels[throttle_channel]=1558
	elif speed =='NORMAL':
		msg.channels[throttle_channel]=1565
	elif speed == 'FAST':
		msg.channels[throttle_channel]=1570
		direction='STRAIGHT'
	if direction =='STRAIGHT':
		msg.channels[steer_channel]=1385
	elif direction =='RIGHT':
		msg.channels[steer_channel]=1450
	elif direction == 'LEFT':
		msg.channels[steer_channel]=1300
	while not rospy.is_shutdown() and flag:
		sample_time=time.time()
	if ((sample_time - start) > exec_time):
		flag=False
	rospy.loginfo(msg)
	pub.publish(msg)
	r.sleep()

if __name__ == '__main__':

	changeMode('MANUAL')
	if 'True' in str(resp1):
		try:
		#talker()
		manualControl('NONE' , 0, 'RIGHT', 50):
	except rospy.ROSInterruptException: pass
