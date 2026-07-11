#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Float32

class FingerDataConverter:
    def __init__(self):
        rospy.init_node('das_controller_converter', anonymous=True)
        
        self.publish_rate = 100  # rospy.get_param('~publish_rate', 50)
        self.latest_left_data = None
        self.latest_left_cmd = None
        
        rospy.Subscriber('/left_finger/encoder', Float32, self.left_finger_data_callback)
        self.left_finger_feedback_pub = rospy.Publisher('/finger/left/current_distance', PoseStamped, queue_size=10)      

        rospy.Subscriber('/target_finger/left_finger', PoseStamped, self.left_cmd_callback)
        self.left_finger_cmd_pub = rospy.Publisher('/left_finger/target_distance', Float32, queue_size=10)

        rospy.loginfo("Finger Data Converter Node Started")
        rospy.loginfo(f"Publish rate: {self.publish_rate}Hz")
    
    def left_finger_data_callback(self, msg):
        """Store latest left finger feedback."""
        self.latest_left_data = msg
    
    def process_finger_feedback(self, finger_msg, publisher, finger_name):
        """Convert Float32 distance to PoseStamped for the model."""
        pose_msg = PoseStamped()
        
        if hasattr(finger_msg, 'header') and finger_msg.header.stamp:
            pose_msg.header.stamp = finger_msg.header.stamp
        else:
            pose_msg.header.stamp = rospy.Time.now()
            
        pose_msg.header.frame_id = f"{finger_name}_finger_frame"
        
        pose_msg.pose.position.x = finger_msg.data
        pose_msg.pose.position.y = 0.0
        pose_msg.pose.position.z = 0.0
        
        pose_msg.pose.orientation.x = 0.0
        pose_msg.pose.orientation.y = 0.0
        pose_msg.pose.orientation.z = 0.0
        pose_msg.pose.orientation.w = 1.0
        
        publisher.publish(pose_msg)

        # Used during calibration
        # self.left_finger_cmd_pub.publish(0.1)
        
        rospy.loginfo(f"Published {finger_name} feedback distance: {finger_msg.data}")

    def left_cmd_callback(self, msg):
        """Store latest left finger command."""
        self.latest_left_cmd = msg
    
    def process_finger_cmd(self, pos_msg, publisher, finger_name):
        """PoseStamped -> Float32 target_distance."""
        finger_cmd_msg = Float32()
        
        finger_cmd_msg.data = pos_msg.pose.position.x
        
        publisher.publish(finger_cmd_msg)
        
        # rospy.loginfo(f"Published {finger_name} command distance: {pos_msg.pose.position.x}")
    
    def publish_all_data(self):
        """Publish at fixed rate."""
        if self.latest_left_data is not None:
            self.process_finger_feedback(self.latest_left_data, self.left_finger_feedback_pub, "left")
        
        if self.latest_left_cmd is not None:
            self.process_finger_cmd(self.latest_left_cmd, self.left_finger_cmd_pub, "left")
    
    def run(self):
        rate = rospy.Rate(self.publish_rate)
        while not rospy.is_shutdown():
            self.publish_all_data()
            rate.sleep()

if __name__ == '__main__':
    try:
        converter = FingerDataConverter()
        converter.run()
    except rospy.ROSInterruptException:
        pass
