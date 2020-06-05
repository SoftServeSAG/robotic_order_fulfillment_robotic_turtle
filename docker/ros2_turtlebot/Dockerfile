FROM ros2_base

WORKDIR /root

RUN apt-get update && apt-get install -y \
    openssh-server \
    gdb \
    gdbserver \
    ros-$ROS_DISTRO-cartographer \
    ros-$ROS_DISTRO-cartographer-ros \
    ros-$ROS_DISTRO-navigation2 \
    ros-$ROS_DISTRO-nav2-bringup \
    ros-$ROS_DISTRO-action-msgs \
    ros-$ROS_DISTRO-ros1-bridge \
    ros-melodic-desktop \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /var/run/sshd
RUN echo 'root:root' | chpasswd
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

RUN echo "source /opt/ros/$ROS_DISTRO/setup.bash" >> ~/.bashrc

RUN mkdir -p ~/deps_ws/src && \
    cd ~/deps_ws && \
    wget https://raw.githubusercontent.com/ROBOTIS-GIT/turtlebot3/ros2/turtlebot3.repos && \
    vcs import src < turtlebot3.repos && \
    . /opt/ros/$ROS_DISTRO/setup.sh &&\
    colcon build --symlink-install

RUN echo "PS1='\[\e[33m\][MrTurtle]\[\e[m\] ${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '" >> ~/.bashrc

RUN echo "source ~/deps_ws/install/setup.bash" >> ~/.bashrc
RUN echo 'export ROS_DOMAIN_ID=30 #TURTLEBOT3' >> ~/.bashrc
RUN echo "export XV_NAME=turtlebot_0" >> ~/.bashrc
