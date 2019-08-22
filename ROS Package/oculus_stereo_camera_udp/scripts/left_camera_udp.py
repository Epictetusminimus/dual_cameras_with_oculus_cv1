#!/usr/bin/env python

import rospy
import sys
import socket
from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np
import base64


class robotSocketServer:
    def __init__(self):
        # Subscribe to left camera topic
        self.left_image_sub = rospy.Subscriber("/left/camera/image_raw/compressed", CompressedImage, self.left_img_cb)

	    # This is the IP and PORT where the node will send the images (e.g. the computer with Oculus)
	    # Remember, every different data needs a different port
	    self.UDP_IP = "192.168.1.119"
	    self.UDP_PORT = 5006

    def send_img(self, eye, ros_data):
	    np_arr = np.fromstring(ros_data.data, np.uint8)
        img_to_send = base64.encodestring(np_arr.tostring())        
	    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(img_to_send, (self.UDP_IP, self.UDP_PORT))
        #print(str(eye) + " image sent.")


    def left_img_cb(self, ros_data):
	    eye = "Left"
        self.send_img(eye, ros_data)

def main(args):
    rospy.init_node('left_camera_udp')
    so = robotSocketServer()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print "Shutting down ROS Image feature detector module"

if __name__ == '__main__':
    main(sys.argv)
