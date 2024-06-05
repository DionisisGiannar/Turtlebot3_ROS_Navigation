#!/usr/bin/env python3

import rospy
# Brings in the SimpleActionClient
import actionlib
# Brings in the .action file and messages used by the move base action
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal


global goals  # [x_goal, ygoal, qx_goal, qy_goal, qz_goal, qw_goal]


def movebase_client(goal_coords):
    """
    Parameters
    ----------
    goal_coords : (x_goal, ygoal, qx_goal, qy_goal, qz_goal, qw_goal)
    """

    # Create an action client called "move_base " with action definition file "MoveBaseAction"
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)

    # Wait until the action server has started and listening for goals.
    client.wait_for_server()

    # Creates a new goal with the MoveBaseGoal constructor
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()

    # Goal Position along the x-axis of the "map" coordinate frame
    goal.target_pose.pose.position.x = goal_coords[0]
    goal.target_pose.pose.position.y = goal_coords[1]

    # Goal Orientation in Quaternions
    goal.target_pose.pose.orientation.x = goal_coords[2]
    goal.target_pose.pose.orientation.y = goal_coords[3]
    goal.target_pose.pose.orientation.z = goal_coords[4]
    goal.target_pose.pose.orientation.w = goal_coords[5]

    # Sends the goal to the action server
    client.send_goal(goal)
    # Wait for the server to finish performing the action
    wait = client.wait_for_result()

    # if the result does not arrive, assume the Server is not available
    if not wait:
        error_msg = "Action server not available!"
        rospy.logerr(error_msg)
        rospy.signal_shutdown(error_msg)
    else:
        # Return the Result of execution the action
        return client.get_result()


if __name__ == "__main__":
    goals = [(0.7, 1.6, 0.0, 0.0, 0.33, 0.94),
             (5.7, -3.9, 0.0, 0.0, -0.44, 0.89),
             (-6.0, -3.1, 0.0, 0.0, -0.29, 0.95)
             ]
    goal_index = 0
    for goal_coords in goals:
        goal_index += 1

        try:
            rospy.init_node("movebase_client_py")
            result = movebase_client(goal_coords)
            
            if result:
                rospy.loginfo(f"Goal {goal_index}: {goal_coords} execution done!")
            else:
                rospy.logerr(f"Goal {goal_index}: {goal_coords} not able to execute. \nExiting...")

        except rospy.ROSInterruptException:
            rospy.loginfo("Navigation test finished.")
