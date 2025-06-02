#!/usr/bin/env python3
"""
Gazebo Simulation Starter for Monocopter Drone
- Connects to Gazebo via ROS
- Spawns a monocopter model
- Publishes control commands to rotate and stabilize
"""

import rospy
from gazebo_msgs.srv import SpawnModel, DeleteModel
from geometry_msgs.msg import Pose, Twist
from std_msgs.msg import Float64
import os

def spawn_monocopter_model():
    # Adjust the path to your SDF or URDF file
    model_path = os.path.join(os.path.dirname(__file__), "models", "monocopter.sdf")
    with open(model_path, 'r') as f:
        model_xml = f.read()

    rospy.wait_for_service('/gazebo/spawn_sdf_model')
    try:
        spawn_model = rospy.ServiceProxy('/gazebo/spawn_sdf_model', SpawnModel)
        pose = Pose()
        pose.position.x = 0
        pose.position.y = 0
        pose.position.z = 1
        spawn_model("monocopter", model_xml, "", pose, "world")
        rospy.loginfo("Monocopter model spawned")
    except rospy.ServiceException as e:
        rospy.logerr(f"Spawn service call failed: {e}")


def control_loop():
    pub_thrust = rospy.Publisher('/monocopter/thrust', Float64, queue_size=1)
    rospy.init_node('monocopter_controller', anonymous=True)
    rate = rospy.Rate(10)  # 10 Hz
    try:
        while not rospy.is_shutdown():
            # Simple hovering command
            thrust = Float64()
            thrust.data = 9.8  # counteract gravity (placeholder)
            pub_thrust.publish(thrust)
            rate.sleep()
    except rospy.ROSInterruptException:
        pass


def main():
    rospy.init_node('gazebo_setup', anonymous=True)
    spawn_monocopter_model()
    control_loop()


if __name__ == "__main__":
    main()
