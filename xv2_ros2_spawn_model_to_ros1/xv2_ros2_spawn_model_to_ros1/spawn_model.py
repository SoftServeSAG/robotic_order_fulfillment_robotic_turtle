# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
import rclpy
from rclpy.parameter import Parameter

import argparse
import math
import os
import sys
from urllib.parse import SplitResult, urlsplit
from xml.etree import ElementTree

from gazebo_msgs.srv import SpawnModel
from geometry_msgs.msg import Pose, Point, Quaternion
import rclpy
from rclpy.node import Node
# from gazebo_ros import gazebo_interface

class SpawnModelNode(Node):

    def __init__(self, args):
        super().__init__('spawn_entity', allow_undeclared_parameters=True,
                         automatically_declare_parameters_from_overrides=True)
        print("I am at init!")

        # self.declare_parameter('file')

        self.entity = self.get_parameter_or('entity', Parameter('entity', Parameter.Type.STRING, 'waffle')).value
        self.file = self.get_parameter_or('file', Parameter('file', Parameter.Type.STRING, "./unknown.urdf")).value
        self.reference_frame = self.get_parameter_or('reference_frame', Parameter('reference_frame', Parameter.Type.STRING, "")).value
        self.gazebo_namespace = self.get_parameter_or('gazebo_namespace', Parameter('gazebo_namespace', Parameter.Type.STRING, "/gazebo")).value
        self.robot_namespace = self.get_parameter_or('robot_namespace', Parameter('robot_namespace', Parameter.Type.STRING, "")).value
        self.unpause = self.get_parameter_or('unpause', Parameter('unpause', Parameter.Type.BOOL, True)).value
        self.sdf = self.get_parameter_or('sdf', Parameter('sdf', Parameter.Type.BOOL, False)).value
        self.wait = self.get_parameter_or('wait', Parameter('wait', Parameter.Type.STRING, "")).value
        self.x = self.get_parameter_or('x', Parameter('x', Parameter.Type.DOUBLE, 0.0)).value
        self.y = self.get_parameter_or('y', Parameter('y', Parameter.Type.DOUBLE, 0.0)).value
        self.z = self.get_parameter_or('z', Parameter('z', Parameter.Type.DOUBLE, 0.0)).value
        self.R = self.get_parameter_or('R', Parameter('R', Parameter.Type.DOUBLE, 0.0)).value
        self.P = self.get_parameter_or('P', Parameter('P', Parameter.Type.DOUBLE, 0.0)).value
        self.Y = self.get_parameter_or('Y', Parameter('Y', Parameter.Type.DOUBLE, 0.0)).value

    def run(self):
        # Load entity XML from file
        if self.file:
            self.get_logger().info('Loading entity XML from file %s' % self.file)
            # if not os.path.exists(str(self.file)):
            #     print("I am at error1!")
            #     # self.get_logger().error('Error: specified file %s does not exist', self.file)
            #     return 1
            if not os.path.isfile(self.file):
                # self.get_logger().error('Error: specified file %s is not a file', str(self.file))
                print("I am at error2")
                return 1
            # load file
            try:
                print("I am at open!")
                f = open(self.file, 'r')
                entity_xml = f.read()
            except IOError as e:
                self.get_logger().error('Error reading file {}: {}'.format(str(self.file), e))
                return 1
            if entity_xml == '':
                print("I am at entity_xml == '':")
                self.get_logger().error('Error: file %s is empty', str(self.file))
                return 1
        # Parse xml to detect invalid xml before sending to gazebo
        try:
            xml_parsed = ElementTree.fromstring(entity_xml)
        except ElementTree.ParseError as e:
            self.get_logger().error('Invalid XML: {}'.format(e))
            return 1

        # Encode xml object back into string for service call
        entity_xml = ElementTree.tostring(xml_parsed)

        print("I am at initial_pose = Pose()")
        # Form requested Pose from arguments
        initial_pose = Pose()
        initial_pose.position.x = float(self.x)
        initial_pose.position.y = float(self.y)
        initial_pose.position.z = float(self.z)

        q = quaternion_from_euler(self.R, self.P, self.Y)
        initial_pose.orientation.w = q[0]
        initial_pose.orientation.x = q[1]
        initial_pose.orientation.y = q[2]
        initial_pose.orientation.z = q[3]

        if self.sdf:
            success = self._spawn_sdf_entity(entity_xml, initial_pose)
        else:
            success = self._spawn_entity(entity_xml, initial_pose)
        if not success:
            self.get_logger().error('Spawn service failed. Exiting.')
            return 1

        return 0

    def _spawn_entity(self, entity_xml, initial_pose):
        self.get_logger().info('Waiting for service %s/spawn_urdf_model' % self.gazebo_namespace)
        self.get_logger().info('SpawnModel type %s' % type(SpawnModel))

        client = self.create_client(SpawnModel, '%s/spawn_urdf_model' % self.gazebo_namespace)
        # self.model_name = self.entity
        # self.model_xml = str(entity_xml, 'utf-8')
        # success = gazebo_interface.spawn_urdf_model_client(self.model_name, model_xml, self.robot_namespace,
        #                                                    initial_pose, self.reference_frame, self.gazebo_namespace)

        if client.wait_for_service(timeout_sec=5.0):
            req = SpawnModel.Request()
            req.model_name = self.entity
            req.model_xml = str(entity_xml, 'utf-8')
            req.robot_namespace = self.robot_namespace
            req.initial_pose = initial_pose
            req.reference_frame = self.reference_frame
            self.get_logger().info('Calling service %s/spawn_urdf_model' % self.gazebo_namespace)
            srv_call = client.call_async(req)
            while rclpy.ok():
                if srv_call.done():
                    self.get_logger().info('Spawn status: %s' % srv_call.result().status_message)
                    break
                rclpy.spin_once(self)
            return srv_call.result().success
        self.get_logger().error(
            'Service %s/spawn_urdf_model unavailable. Was Gazebo started with GazeboRosFactory?')
        return False

    def _spawn_sdf_entity(self, entity_xml, initial_pose):
        self.get_logger().info('Waiting for service %s/spawn_sdf_model' % self.gazebo_namespace)
        client = self.create_client(SpawnModel, '%s/spawn_sdf_model' % self.gazebo_namespace)
        if client.wait_for_service(timeout_sec=5.0):
            req = SpawnModel.Request()
            req.model_name = self.entity
            req.model_xml = str(entity_xml, 'utf-8')
            req.robot_namespace = self.robot_namespace
            req.initial_pose = initial_pose
            req.reference_frame = self.reference_frame
            self.get_logger().info('Calling service %s/spawn_sdf_model' % self.gazebo_namespace)
            srv_call = client.call_async(req)
            while rclpy.ok():
                if srv_call.done():
                    self.get_logger().info('Spawn status: %s' % srv_call.result().status_message)
                    break
                rclpy.spin_once(self)
            return srv_call.result().success
        self.get_logger().error(
            'Service %s/spawn_sdf_model unavailable. Was Gazebo started with GazeboRosFactory?')
        return False


def quaternion_from_euler(roll, pitch, yaw):
    cy = math.cos(yaw * 0.5)
    sy = math.sin(yaw * 0.5)
    cp = math.cos(pitch * 0.5)
    sp = math.sin(pitch * 0.5)
    cr = math.cos(roll * 0.5)
    sr = math.sin(roll * 0.5)

    q = [0] * 4
    q[0] = cy * cp * cr + sy * sp * sr
    q[1] = cy * cp * sr - sy * sp * cr
    q[2] = sy * cp * sr + cy * sp * cr
    q[3] = sy * cp * cr - cy * sp * sr

    return q


def spawn(args=sys.argv):
    rclpy.init(args=args)
    args_without_ros = rclpy.utilities.remove_ros_args(args)
    spawn_entity_node = SpawnModelNode(args_without_ros)
    spawn_entity_node.get_logger().info('Spawn Entity started')
    exit_code = spawn_entity_node.run()
    sys.exit(exit_code)


if __name__ == '__main__':
    spawn()
