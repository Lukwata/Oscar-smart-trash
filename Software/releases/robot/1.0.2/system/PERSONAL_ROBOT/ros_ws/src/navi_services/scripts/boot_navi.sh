#!/bin/bash

echo "" > ip.txt
rm -f .done

while [ ! -f .done ]; do
	ip=`ifconfig wlan0 | awk '/inet addr/{print substr($2,6)}' | grep -v "127.0.0.1" | head -1`
	old_ip=`head -1 ip.txt`

	if [ "$ip" == "" ]; then
		echo "wait for wifi"
	elif [ "$ip" == "$old_ip" ]; then
		echo "ok: `date`"
		sleep 60
	else
		echo "update new ip: $ip"
		echo "$ip" > ip.txt

		ros_build=$HOME/aos/system/$DEVICE_TYPE/ros_ws/build
        if [ ! -d $ros_build ]
        then
            cd ~/aos/system/PERSONAL_ROBOT/ros_ws/ && sudo chmod a+x src/navi_services/src/* && sudo chmod a+x src/navi_services/scripts/* && sudo chmod a+x src/pr_teleop/src/* && sudo chmod a+x src/virtual_cam/src/* && catkin_make
        fi

		echo "export ROS_IP=$ip" > ~/set_params.sh
		echo "export ROS_MASTER_URI=http://$ip:11311" >> ~/set_params.sh
		echo "export ROS_HOSTNAME=$ip" >> ~/set_params.sh
		echo "source $HOME/aos/system/PERSONAL_ROBOT/ros_ws/devel/setup.bash" >> ~/set_params.sh
		echo "export ROS_PACKAGE_PATH=$HOME/aos/system/PERSONAL_ROBOT/ros_ws/modified_packages:$ROS_PACKAGE_PATH"
		# echo "clean navi session"
		tmux kill-window -t navi:demo
		sleep 30
		echo "start new navi session"
		###################################
		tmux new-window -n demo -d
		tmux split-window -v -t navi:demo.0
		tmux split-window -v -t navi:demo.1
		##### 4 windows
		tmux split-window -h -t navi:demo.0
		tmux split-window -h -t navi:demo.1

                tmux split-window -h -t navi:demo.4
                
                tmux split-window -h -t navi:demo.0
                tmux split-window -h -t navi:demo.1


		## send to 4 windows commands
		tmux send-keys -t navi:demo.0 'sleep 1; source ~/set_params.sh; roscore' C-m
		tmux send-keys -t navi:demo.1 'sleep 5; source ~/set_params.sh; roslaunch navi_services navi_services.launch' C-m
		tmux send-keys -t navi:demo.2 'sleep 3; source ~/set_params.sh; roscd navi_services; cd src; python navi_bridge.py' C-m
		tmux send-keys -t navi:demo.3 'sleep 8; source ~/set_params.sh; roslaunch pr_teleop pr_move_service.launch' C-m
                #tmux send-keys -t navi:demo.4 'sleep 15; source ~/set_params.sh; cd ~/aos/system/PERSONAL_ROBOT/ros_ws/src/navigation/move_base/launch; roslaunch move_base.launch' C-m
                #tmux send-keys -t navi:demo.5 'sleep 10; source ~/set_params.sh; cd ~/aos/system/PERSONAL_ROBOT/ros_ws/src/navigation/robot_pose_ekf/launch; roslaunch robot_pose_ekf.launch' C-m
                
                #tmux send-keys -t navi:demo.6 'sleep 0; sudo su; echo 1 > /sys/devices/system/cpu/cpu0/online; echo 1 > /sys/devices/system/cpu/cpu0/online; echo 1 > /sys/devices/system/cpu/cpu2/online; echo 1 > /sys/devices/system/cpu/cpu3/online' C-m
                #while true
                #do  tmux send-keys -t navi:demo.6 'sleep 35; rosrun map_server map_saver map:=map' C-m
                #done &               
                #tmux send-keys -t navi:demo.7 'sleep 2; cd; sudo rm Public/rtabmap.db' C-m

		#tmux send-keys -t navi:demo.4 'sudo modprobe -r v4l2loopback' C-m
		#sleep 3
		#tmux send-keys -t navi:demo.4 'sudo modprobe v4l2loopback video_nr=0 exclusive_caps=1' C-m
		#sleep 3
		#tmux send-keys -t navi:demo.4 'sleep 15; source ~/set_params.sh; rosrun virtual_cam stream _device:=/dev/video0 _width:=640 _height:=480 _fourcc:=YUYV image:=/camera/rgb/image_raw' C-m

	fi
	sleep 1
done
