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

class SpawnModelNode(Node):

    def __init__(self, args):
        super().__init__('spawn_entity')
        parser = argparse.ArgumentParser(
            description='Spawn an entity in gazebo. Gazebo must be started with gazebo_ros_init,\
            gazebo_ros_factory and gazebo_ros_state for all functionalities to work')

        source = parser.add_mutually_exclusive_group(required=True)
        source.add_argument('-file', type=str, metavar='FILE_NAME',
                            help='Load entity xml from file')

        parser.add_argument('-entity', required=True, type=str, metavar='ENTITY_NAME',
                            help='Name of entity to spawn')

        parser.add_argument('-reference_frame', type=str, default='',
                            help='Name of the model/body where initial pose is defined.\
                            If left empty or specified as "world", gazebo world frame is used')

        parser.add_argument('-gazebo_namespace', type=str, default='',
                            help='ROS namespace of gazebo offered ROS interfaces. \
                            Default is without any namespace')

        parser.add_argument('-robot_namespace', type=str, default=self.get_namespace(),
                            help='change ROS namespace of gazebo-plugins')

        parser.add_argument('-unpause', action='store_true',
                            help='unpause physics after spawning entity')

        parser.add_argument('-sdf', dest='sdf', action='store_true',
                            help='Spawn sdf model')

        parser.add_argument('-wait', type=str, metavar='ENTITY_NAME',
                            help='Wait for entity to exist')
        parser.add_argument('-x', type=float, default=0,
                            help='x component of initial position, meters')
        parser.add_argument('-y', type=float, default=0,
                            help='y component of initial position, meters')
        parser.add_argument('-z', type=float, default=0,
                            help='z component of initial position, meters')
        parser.add_argument('-R', type=float, default=0,
                            help='roll angle of initial orientation, radians')
        parser.add_argument('-P', type=float, default=0,
                            help='pitch angle of initial orientation, radians')
        parser.add_argument('-Y', type=float, default=0,
                            help='yaw angle of initial orientation, radians')

        self.args = parser.parse_args(args[1:])

    def run(self):
        # Load entity XML from file
        if self.args.file:
            self.get_logger().info('Loading entity XML from file %s' % self.args.file)
            if not os.path.exists(self.args.file):
                self.get_logger().error('Error: specified file %s does not exist', self.args.file)
                return 1
            if not os.path.isfile(self.args.file):
                self.get_logger().error('Error: specified file %s is not a file', self.args.file)
                return 1
            # load file
            try:
                f = open(self.args.file, 'r')
                entity_xml = f.read()
            except IOError as e:
                self.get_logger().error('Error reading file {}: {}'.format(self.args.file, e))
                return 1
            if entity_xml == '':
                self.get_logger().error('Error: file %s is empty', self.args.file)
                return 1
        # Parse xml to detect invalid xml before sending to gazebo
        try:
            xml_parsed = ElementTree.fromstring(entity_xml)
        except ElementTree.ParseError as e:
            self.get_logger().error('Invalid XML: {}'.format(e))
            return 1

        # Encode xml object back into string for service call
        entity_xml = ElementTree.tostring(xml_parsed)

        # Form requested Pose from arguments
        initial_pose = Pose()
        initial_pose.position.x = float(self.args.x)
        initial_pose.position.y = float(self.args.y)
        initial_pose.position.z = float(self.args.z)

        q = quaternion_from_euler(self.args.R, self.args.P, self.args.Y)
        initial_pose.orientation.w = q[0]
        initial_pose.orientation.x = q[1]
        initial_pose.orientation.y = q[2]
        initial_pose.orientation.z = q[3]

        if self.args.sdf:
            success = self._spawn_sdf_entity(entity_xml, initial_pose)
        else:
            success = self._spawn_entity(entity_xml, initial_pose)
        if not success:
            self.get_logger().error('Spawn service failed. Exiting.')
            return 1

        return 0

    def _spawn_entity(self, entity_xml, initial_pose):
        self.get_logger().info('Waiting for service %s/spawn_urdf_model' % self.args.gazebo_namespace)
        client = self.create_client(SpawnModel, '%s/spawn_urdf_model' % self.args.gazebo_namespace)
        if client.wait_for_service(timeout_sec=5.0):
            req = SpawnModel.Request()
            req.model_name = self.args.entity
            req.model_xml = str(entity_xml, 'utf-8')
            req.robot_namespace = self.args.robot_namespace
            req.initial_pose = initial_pose
            req.reference_frame = self.args.reference_frame
            self.get_logger().info('Calling service %s/spawn_urdf_model' % self.args.gazebo_namespace)
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
        self.get_logger().info('Waiting for service %s/spawn_sdf_model' % self.args.gazebo_namespace)
        client = self.create_client(SpawnModel, '%s/spawn_sdf_model' % self.args.gazebo_namespace)
        if client.wait_for_service(timeout_sec=5.0):
            req = SpawnModel.Request()
            req.model_name = self.args.entity
            req.model_xml = str(entity_xml, 'utf-8')
            req.robot_namespace = self.args.robot_namespace
            req.initial_pose = initial_pose
            req.reference_frame = self.args.reference_frame
            self.get_logger().info('Calling service %s/spawn_sdf_model' % self.args.gazebo_namespace)
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
