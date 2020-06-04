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


Init workspace

```bash
mkdir -p ws/src
cd ws/src
git clone https://github.com/SoftServeSAG/order_fullfilement_robotic_arm.git
```

Create docker net
```bash
sudo docker network create --driver=bridge --subnet=178.18.0.0/16 ros_net
```

Build docker images

```bash
cd order_fullfilement_robotic_arm/docker/
cd ros2_base
sudo ./build.bash 
cd ../ros2_turtlebot_ws/
sudo ./build.bash 
```

Run docker container

```bash
sudo ./run.bash
```

Inside docker container
