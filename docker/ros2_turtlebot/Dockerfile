FROM lyubomyrd/robotics_ros2_docker:latest

WORKDIR /root

RUN set -x && \
    echo "Upgrading Gazebo 9 to latest release" && \
    echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable `lsb_release -cs` main" > /etc/apt/sources.list.d/gazebo-stable.list && \
    wget http://packages.osrfoundation.org/gazebo.key -O - | apt-key add - && \
    apt-get update && \
    apt-get remove -y gazebo* && \
    apt-get install -y libgazebo9 

RUN apt-get update && apt-get install -y \
    openssh-server \
    gdb \
    gdbserver \
    python3-vcstool \
    #ros-$ROS_DISTRO-cartographer \
    #ros-$ROS_DISTRO-cartographer-ros \
    #ros-$ROS_DISTRO-navigation2 \
    #ros-$ROS_DISTRO-nav2-bringup \
    ros-$ROS_DISTRO-action-msgs \
    ros-$ROS_DISTRO-gazebo-msgs\
    ros-$ROS_DISTRO-gazebo-ros-pkgs \
    ros-$ROS_DISTRO-ros1-bridge\
    ros-noetic-desktop \
    ros-noetic-turtlebot3-msgs \
    ros-noetic-gazebo-msgs\
    libzbar-dev \
    libzbar0 \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get upgrade -y

RUN mkdir /var/run/sshd
RUN echo 'root:root' | chpasswd
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

RUN echo "source /opt/ros/$ROS_DISTRO/setup.bash" >> ~/.bashrc

RUN mkdir -p ~/deps_ws/src && \
    cd ~/deps_ws && \
    wget https://raw.githubusercontent.com/ROBOTIS-GIT/turtlebot3/ros2/turtlebot3.repos && \
    vcs import src < turtlebot3.repos && \
#hack for using turtlebot urdf model for ROS1
    cd ~/deps_ws/src/turtlebot3 && \
    rm -r ./turtlebot3 && \
    git clone -b ros2 --single-branch https://github.com/yfedi/turtlebot3.git
#end of hack

RUN mkdir -p ~/ros1_ws/src && \
    cd ~/ros1_ws/src && \
    git clone https://github.com/SoftServeSAG/robotics_ros1_bridge_srv.git && \
    cd ~/ros1_ws

RUN /bin/bash -c '. /opt/ros/noetic/setup.bash; cd ~/ros1_ws; catkin_make_isolated --install'

#RUN cd ~/ws
#RUN /bin/bash -c '. /opt/ros/foxy/setup.bash; colcon build --symlink-install --packages-skip ros1_bridge'

#RUN /bin/bash -c 'source /opt/ros/noetic/setup.bash; . /opt/ros/foxy/setup.bash; . ~/ros1_ws/install_isolated/setup.bash  . ~/ws/install/local_setup.bash'

#RUN /bin/bash -c 'colcon build --packages-select ros1_bridge --cmake-force-configure'


# colcon build --symlink-install --packages-select ros1_bridge --cmake-force-configure --cmake-clean-first --cmake-clean-cache




RUN echo "PS1='\[\e[33m\][MrTurtle]\[\e[m\] ${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '" >> ~/.bashrc

# link ~/deps_ws/src/ to ~/ws/src folder
RUN echo "ln -sf ~/deps_ws/src/* ~/ws/src/" >> ~/.bashrc

RUN echo "source ~/ws/install/local_setup.bash" >> ~/.bashrc
RUN echo 'export ROS_DOMAIN_ID=30 #TURTLEBOT3' >> ~/.bashrc
RUN echo "export XV_NAME=turtlebot_0" >> ~/.bashrc
