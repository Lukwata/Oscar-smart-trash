#!/bin/bash

echo "" > ip.txt
rm -f .done

while [ ! -f .done ]; do
	ip=`ifconfig wlan1 | awk '/inet addr/{print substr($2,6)}' | grep -v "127.0.0.1" | head -1`
	old_ip=`head -1 ip.txt`

	if [ "$ip" == "" ]; then
		echo "wait for wifi"
	elif [ "$ip" == "$old_ip" ]; then
		echo "ok: `date`"
		sleep 60
	else
		echo "update new ip: $ip"
		echo "$ip" > ip.txt

		ros_build=$HOME/aos/system/PERSONAL_ROBOT/ros_ws/build
        if [ ! -d $ros_build ]
        then
            cd ~/aos/system/PERSONAL_ROBOT/ros_ws/ 
               #&& sudo chmod a+x src/navi_services/src/* && sudo chmod a+x src/navi_services/scripts/* && sudo chmod a+x src/pr_teleop/src/* && sudo chmod a+x src/virtual_cam/src/* && catkin_make
        fi

		echo "export ROS_IP=$ip" > ~/set_params.sh
		echo "export ROS_MASTER_URI=http://$ip:11311" >> ~/set_params.sh
		echo "export ROS_HOSTNAME=$ip" >> ~/set_params.sh
		#echo "source $HOME/aos/system/PERSONAL_ROBOT/ros_ws/devel/setup.bash" >> ~/set_params.sh
		#echo "export ROS_PACKAGE_PATH=$HOME/aos/system/PERSONAL_ROBOT/ros_ws/modified_packages:$ROS_PACKAGE_PATH"
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
		tmux send-keys -t navi:demo.2 'sleep 3; source ~/set_params.sh; cd /opt/ros/indigo/share/navi_services/scripts; python navi_bridge.py' C-m
		tmux send-keys -t navi:demo.3 'sleep 8; source ~/set_params.sh; roslaunch pr_teleop pr_move_service.launch' C-m

                #tmux send-keys -t navi:demo.5 'sleep 10; cd; clean; source ~/set_params.sh; roslaunch clone_bringup speedup.launch' C-m


	fi
	sleep 1
done
