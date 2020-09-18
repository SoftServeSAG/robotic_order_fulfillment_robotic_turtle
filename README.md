# order_fullfilement_robotic_arm
Robotic Order Fulfillment

## Install
Install nvidia-docker 
```bash
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | \
  sudo apt-key add -
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
  sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get update
sudo apt-get install nvidia-docker2
sudo systemctl restart docker
```


### Init workspace

```bash
mkdir -p turtlebot_ws/src
cd turtlebot_ws/src
git clone git@github.com:SoftServeSAG/robotic_order_fulfillment_robotic_turtle.git
git clone -b foxy --single-branch https://github.com/ros2/ros1_bridge.git
```

Create docker net
```bash
sudo docker network create --driver=bridge --subnet=178.18.0.0/16 ros_net
```

Build docker images

```bash
cd robotic_order_fulfillment_robotic_turtle/docker/ros2_turtlebot/
sudo ./build.bash 
```

Run docker container

```bash
sudo ./run.bash
```

Inside docker container build available packages

```bash
cd ~/ws
colcon build --symlink-install --packages-skip ros1_bridge
source /opt/ros/noetic/setup.bash
. ~/ws/install/local_setup.bash
colcon build --symlink-install --packages-select ros1_bridge --cmake-force-configure --cmake-clean-first --cmake-clean-cache
. ~/ws/install/local_setup.bash
```

Check if ros1_bridge has been built correctly and with all needed messages
```bash
ros2 run ros1_bridge dynamic_bridge --print-pairs
```


### Run 
```bash
cd ~/ws/src/robotic_order_fulfillment_robotic_turtle/scripts
./start.sh
```


## Spawn turtlebot model to ROS1 simulation
For spawning model to ROS1 simulation application ros2_spawn_robot_to_ros1 has been created.

### Application Usage
usage: spawn [-h] -file FILE_NAME -entity ENTITY_NAME
             [-reference_frame REFERENCE_FRAME]
             [-gazebo_namespace GAZEBO_NAMESPACE]
             [-robot_namespace ROBOT_NAMESPACE] [-unpause] [-sdf]
             [-x X] [-y Y] [-z Z] [-R R] [-P P] [-Y Y]

```bash
Spawn an entity in gazebo. Gazebo must be started with gazebo_ros_init,
gazebo_ros_factory and gazebo_ros_state for all functionalities to work
  -h, --help            show this help message and exit
  -file FILE_NAME       Load entity xml from file
  -entity ENTITY_NAME   Name of entity to spawn
  -reference_frame REFERENCE_FRAME
                        Name of the model/body where initial pose is defined.
                        If left empty or specified as "world", gazebo world
                        frame is used
  -gazebo_namespace GAZEBO_NAMESPACE
                        ROS namespace of gazebo offered ROS interfaces.
                        Default is without any namespace
  -robot_namespace ROBOT_NAMESPACE
                        change ROS namespace of gazebo-plugins
  -unpause              unpause physics after spawning entity
  -sdf                  Spawn sdf model
  -wait ENTITY_NAME     Wait for entity to exist
  -x X                  x component of initial position, meters
  -y Y                  y component of initial position, meters
  -z Z                  z component of initial position, meters
  -R R                  roll angle of initial orientation, radians
  -P P                  pitch angle of initial orientation, radians
  -Y Y                  yaw angle of initial orientation, radians
```

Typical command to spawn sdf model:
```bash
ros2 run ros2_spawn_model_to_ros1 spawn -entity entity -file ~/deps_ws/src/turtlebot3/turtlebot3_simulations/turtlebot3_gazebo/models/turtlebot3_waffle_pi/model.sdf -sdf -gazebo_namespace gazebo -x 2
```

Typical command to spawn urdf model:
```bash
ros2 run ros2_spawn_model_to_ros1 spawn -entity entity -file ~/deps_ws/src/turtlebot3/turtlebot3/turtlebot3_description_ros1/urdf/turtlebot3_waffle_pi.urdf -gazebo_namespace gazebo
```

Spawn turtlebot model with top plate with aruco markers
```bash
ros2 run ros2_spawn_model_to_ros1 spawn -entity turtlebot -file ~/ws/src/order_fullfilement_robotic_arm/turtlebot_description/urdf/turtlebot.urdf -gazebo_namespace gazebo -x 0.07 -y 0.68 -z 0.01 -Y -1.6
```
