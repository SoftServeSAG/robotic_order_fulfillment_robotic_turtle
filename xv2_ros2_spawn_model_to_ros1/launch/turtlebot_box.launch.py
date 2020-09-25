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

#TURTLEBOT3_MODEL = os.environ['TURTLEBOT3_MODEL']
# TURTLEBOT3_MODEL = 'waffle'

# def generate_launch_description():
#     use_sim_time = LaunchConfiguration('use_sim_time', default='True')
#     xpos = LaunchConfiguration('x', default=0)
#     launch_file_dir = os.path.join(get_package_share_directory('turtlebot3_gazebo'), 'launch')
#
#     return LaunchDescription([
#         ExecuteProcess(
#             cmd=['ros2', 'param', 'set', '/gazebo', 'use_sim_time', use_sim_time],
#             output='screen'),
#
# 	ExecuteProcess(
#             cmd=['ros2', 'run', 'xv2_ros2_spawn_model_to_ros1', 'spawn'],
#             output='screen'),
#
#         IncludeLaunchDescription(
#             PythonLaunchDescriptionSource([launch_file_dir, '/robot_state_publisher.launch.py']),
#             launch_arguments={'use_sim_time': use_sim_time}.items(),
#         ),
#     ])


def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default='True')
    return launch.LaunchDescription([

        # launch.actions.DeclareLaunchArgument(
        #     'entity',
        #     default_value='entity'),
        # launch.actions.DeclareLaunchArgument(
        #     'file',
        #     default_value='~/deps_ws/src/turtlebot3/turtlebot3/turtlebot3_description/urdf/turtlebot3_waffle_pi.urdf',
        #     description='Path to UDRF file'),
        # launch.actions.DeclareLaunchArgument(
        #     'gazebo_namespace',
        #     default_value='gazebo'),
        ExecuteProcess(
                        cmd=['ros2', 'param', 'set', '/gazebo', 'use_sim_time', use_sim_time],
                        output='screen'),
        launch_ros.actions.Node(
            package='xv2_ros2_spawn_model_to_ros1', executable='spawn_model', output='screen',
            #name=[launch.substitutions.LaunchConfiguration('entity'), 'talker']),
            name='spawn_entity',
            parameters=[
                {'entity': 'waffle2'},
                # {'file': '/root/deps_ws/src/turtlebot3/turtlebot3/turtlebot3_description/urdf/turtlebot3_waffle.urdf'},
                {'file': '/root/ws/src/robotic_order_fulfillment_robotic_turtle/xv2_description/urdf/fake_turtle.urdf.xacro'},
                {'gazebo_namespace': '/gazebo'},
                {'x': 5},
                {'y': 0},
                {'z': 0.0},
            ]),
    ])

# ros2 run ros2_spawn_model_to_ros1 spawn -entity entity -file ~/deps_ws/src/turtlebot3/turtlebot3/turtlebot3_description/urdf/turtlebot3_waffle_pi.urdf -gazebo_namespace gazebo