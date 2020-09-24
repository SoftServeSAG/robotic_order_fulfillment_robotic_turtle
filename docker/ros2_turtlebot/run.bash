#!/usr/bin/env bash


SCRIPT_PATH=$(readlink -f "$0")
SCRIPT_DIR_PATH=$(dirname "$SCRIPT_PATH")
WS_DIR_PATH=$(realpath "$SCRIPT_DIR_PATH/../../../..")

xhost +local:root

docker run -it --rm \
    --privileged \
    --volume=/tmp/.X11-unix:/tmp/.X11-unix \
    --volume="$WS_DIR_PATH:/root/ws" \
    -v /dev/bus/usb:/dev/bus/usb \
    --env="DISPLAY=$DISPLAY" \
    --env QT_X11_NO_MITSHM=1 \
    --add-host hand_0:178.18.0.253 \
    --add-host hand_1:178.18.0.252 \
    --add-host simulation:178.18.0.254 \
    --add-host turtlebot_1:178.18.0.250 \
    --hostname turtlebot_0 \
    --net ros_net \
    --ip 178.18.0.251 \
   ros2_turtlebot_ws

    #--device=/dev/dri:/dev/dri \
    #--device /dev/video2 \

    # --runtime=nvidia \

xhost -local:root
