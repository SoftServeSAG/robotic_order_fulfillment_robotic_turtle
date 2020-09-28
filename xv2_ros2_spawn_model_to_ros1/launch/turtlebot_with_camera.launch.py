#!/usr/bin/env python3

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import ThisLaunchFileDir
from launch.actions import ExecuteProcess
from launch.substitutions import LaunchConfiguration
import launch
import launch.actions
import launch.substitutions
import launch_ros.actions


def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default='True')
    return launch.LaunchDescription([

        ExecuteProcess(
                        cmd=['ros2', 'param', 'set', '/gazebo', 'use_sim_time', use_sim_time],
                        output='screen'),

        launch_ros.actions.Node(
            package='xv2_ros2_spawn_model_to_ros1', executable='spawn_model', output='screen',
            #name=[launch.substitutions.LaunchConfiguration('entity'), 'talker']),
            name='spawn_entity',
            parameters=[
                      {'entity': 'waffle'},
                      {'file': '/root/ws/src/turtlebot3/turtlebot3/turtlebot3_description_ros1/urdf/turtlebot3_waffle_pi_with_box.urdf'},
                      {'gazebo_namespace': '/gazebo'},
                      {'x': 0.0},
                      {'y': 0.55},
                      {'z': 0.0},
                  ]),




    ])

# ros2 run ros2_spawn_model_to_ros1 spawn -entity entity -file ~/deps_ws/src/turtlebot3/turtlebot3/turtlebot3_description/urdf/turtlebot3_waffle_pi.urdf -gazebo_namespace gazebo