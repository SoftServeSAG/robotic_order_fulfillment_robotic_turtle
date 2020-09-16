import os
from glob import glob
from setuptools import setup

package_name = 'xv2_ros2_spawn_model_to_ros1'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    # data_files=[
    #     ('share/ament_index/resource_index/packages',
    #         ['resource/' + package_name]),
    #     ('share/' + package_name, ['package.xml']),
    #     ('share/' + package_name, ['launch/turtlebot.launch.py']),
    # ],
    py_modules=[
        package_name + '/spawn_model'],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        # Include our package.xml file
        (os.path.join('share', package_name), ['package.xml']),
        # Include all launch files.
        # (os.path.join('share', package_name, 'launch'), glob('*.launch.py')),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        # ('share/' + package_name, ['launch/turtlebot.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    include_package_data=True,
    maintainer='root',
    maintainer_email='root@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'spawn_model = ' + package_name + '.spawn_model:spawn'
        ],
    },
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        # "": ["*.txt", "*.rst"],
        # And include any *.msg files found in the "hello" package, too:
        # package_name: ["*launch*"],
    },
)