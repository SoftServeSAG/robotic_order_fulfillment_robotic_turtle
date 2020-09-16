from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='xv2_usb_camera',
            node_namespace='turtle_0',
            node_executable='usb_cam_driver',
            node_name='usb_cam_driver'
        )
    ])