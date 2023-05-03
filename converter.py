#!/usr/bin/env python3

#import the dependencies
 
import rospy
from geometry_msgs.msg import Twist
from unitree_legged_msgs.msg import HighCmd
import numpy as np
from std_msgs.msg import Bool

class ConvertCmdHigh:
    def __init__(self):
        self.pub = rospy.Publisher('/high_cmd',HighCmd,queue_size=1)
        self.sub_cmd_vel =  rospy.Subscriber("/cmd_vel", Twist, self.cmd_callback)
        self.high_cmd = HighCmd()
        self.sub_emerg_stop =  rospy.Subscriber("/eme_stop", Bool, self.emer_stop_callback)
        self.stop = 0

    def emer_stop_callback(self,msg):
        if msg.data:
            self.stop = msg.data

    def cmd_callback(self, msg):
        if msg and not self.stop:
            self.high_cmd.mode = 2      # 0:idle, default stand      1:forced stand     2:walk continuously
            self.high_cmd.gaitType = 1
            self.high_cmd.speedLevel = 0
            self.high_cmd.footRaiseHeight = 0.1
            self.high_cmd.bodyHeight = 0.1
            self.high_cmd.euler = [0, 0, 0]
            self.high_cmd.velocity = [msg.linear.x , msg.linear.y]
            self.high_cmd.yawSpeed = msg.angular.z 
            self.high_cmd.reserve = 0
          
            self.pub.publish(self.high_cmd)
        else: 

            self.high_cmd.mode = 0      # 0:idle, default stand      1:forced stand     2:walk continuously
            self.high_cmd.gaitType = 0
            self.high_cmd.speedLevel = 0
            self.high_cmd.footRaiseHeight = 0
            self.high_cmd.bodyHeight = 0
            self.high_cmd.euler = [0, 0, 0]
            self.high_cmd.velocity = [0, 0]
            self.high_cmd.yawSpeed = 0.0
            self.high_cmd.reserve = 0

            self.pub.publish(self.high_cmd)
if __name__=="__main__":

    #initialise the node
	rospy.init_node("converter", anonymous=True)
	conv = ConvertCmdHigh()

	#while the node is still on
	r = rospy.Rate(10)
	while not rospy.is_shutdown():
		r.sleep()
                
###  to set forced state just these two else else
#     cmd.mode = 1;
#     cmd.bodyHeight = -0.2;
#   }
#   if (motiontime > 7000 && motiontime < 8000)
#   {
#     cmd.mode = 1;
#     cmd.bodyHeight = 0.1;
