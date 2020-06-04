#!/usr/bin/env bash


SCRIPT_PATH=$(readlink -f "$0")
SCRIPT_DIR_PATH=$(dirname "$SCRIPT_PATH")
WS_DIR_PATH=$(realpath "$SCRIPT_DIR_PATH/../../../..")

xhost +local:root

docker run -it --rm \
    --privileged \
    --volume=/tmp/.X11-unix:/tmp/.X11-unix \
    --volume="$WS_DIR_PATH:/root/ws" \
    --device=/dev/dri:/dev/dri \
    --env="DISPLAY=$DISPLAY" \
    --env QT_X11_NO_MITSHM=1 \
    --add-host simulation:178.18.0.2 \
    --add-host turtlebot_1:178.18.0.7 \
    --hostname turtlebot_0 \
    --net ros_net \
    --ip 178.18.0.6 \
   ros2_gazebo_8_ws


xhost -local:root
