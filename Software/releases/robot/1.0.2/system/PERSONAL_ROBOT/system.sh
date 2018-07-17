#!/bin/bash

# load apps at startup by default
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib/

tmux has-session -t autonomous
if [ $? != 0 ]; then

    tmux new-session -s autonomous -n os -d
    tmux split-window -v -t autonomous
    tmux split-window -v -t autonomous:os.0
    tmux split-window -v -t autonomous:os.1
    tmux split-window -h -t autonomous:os.2

    #start Animation:
    tmux send-keys -t autonomous:os.1 'python $HOME/aos/ability/animation/UI/main.py' C-m

    #run boot os for all device:
    tmux send-keys -t autonomous:os.0 'cd $HOME/aos/system && python setup.py' C-m

    #start navi:
    tmux new-session -s navi -n ros -d
    tmux split-window -v -t navi
    tmux send-keys -t navi:ros.0 'cd /home/ubuntu/aos/system/PERSONAL_ROBOT/ros_ws/src/navi_services/scripts && bash boot_navi.sh' C-m


fi
