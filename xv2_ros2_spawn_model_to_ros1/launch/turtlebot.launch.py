#!/usr/bin/env python3

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import ThisLaunchFileDir
from launch.actions import ExecuteProcess
from launch.substitutions import LaunchConfiguration

#TURTLEBOT3_MODEL = os.environ['TURTLEBOT3_MODEL']
TURTLEBOT3_MODEL = 'waffle'

def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default='True')
    xpos = LaunchConfiguration('x', default=0)
    launch_file_dir = os.path.join(get_package_share_directory('turtlebot3_gazebo'), 'launch')

    return LaunchDescription([
        ExecuteProcess(
            cmd=['ros2', 'param', 'set', '/gazebo', 'use_sim_time', use_sim_time],
            output='screen'),

	ExecuteProcess(
            cmd=['ros2', 'run', 'xv2_ros2_spawn_model_to_ros1', 'spawn'],
            output='screen'),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([launch_file_dir, '/robot_state_publisher.launch.py']),
            launch_arguments={'use_sim_time': use_sim_time}.items(),
        ),
    ])