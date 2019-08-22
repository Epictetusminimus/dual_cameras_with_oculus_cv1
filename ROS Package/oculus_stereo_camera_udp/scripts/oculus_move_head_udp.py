#!/usr/bin/env python

import rospy
import sys
import socket
from sensor_msgs.msg import CompressedImage

#For the desktop robot:
from arduino_servo_msg.msg import servo

#For the pioneer robot:
from corobot_msgs.msg import ServoPosition

def oculusToDegrees(value):
    # Range of the purple robot: 10 - 130 degrees
    oldRange = 1.0
    NewRange = 120.0
    if(value > 0.5):
        value = 0.5
    if(value < -0.5):
        value = -0.5
    return (((value + 0.5)*NewRange)/oldRange) + 10.0

def move_robot_head():
    # If you want to control the motors in the Desktop Robot uncomment the line below:
    servo_pub = rospy.Publisher('/moveYaw', servo, queue_size=1)
	
	# This topic is for the Pioneer robot
	#servo_pub = rospy.Publisher('/phidgetServo_setPosition', ServoPosition, queue_size=1)
	
    rospy.init_node('oculus_move_head')
    rate = rospy.Rate(120)

	# This IP and PORT if for the computer in the robot (do not put the IP from the Oculus server)!!
    UDP_IP = "192.168.1.106" 
    UDP_PORT = 5007

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    while not rospy.is_shutdown():
        data, addr = sock.recvfrom(64)
        rot = data.split()
		
		#if using the desktop robot:
		rotY = float(rot[1])
        rotMotorX = oculusToDegrees(rotY)
        servo_pub.publish(int(rotMotorX), 40.0)
		
		#if using the pioneer robot:
		#rotX = float(rot[0])
		#rotY = float(rot[1])
        #rotMotorX = oculusToDegrees(rotY)
		#rotMotorY = oculusToDegrees(rotX)
        #servo_pub.publish(6, float(rotMotorY))
		#servo_pub.publish(7, float(rotMotorX))
        
        rate.sleep()
            

def main(args):
    try:
        move_robot_head()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main(sys.argv)
