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
    tmux split-window -h -t autonomous:os.3


    #run boot os for all device:
    tmux send-keys -t autonomous:os.0 'cd $HOME/aos/system && python setup.py' C-m

    #run user manager for all device:
    sudo setterm -blank 0 -powerdown 0
    sudo startx /usr/bin/eog -f /home/pi/img/main.jpg &
fi
