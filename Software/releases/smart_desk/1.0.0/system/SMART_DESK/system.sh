#!/bin/bash

# load apps at startup by default
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib/

tmux has-session -t autonomous
if [ $? != 0 ]; then

    tmux new-session -s autonomous -n os -d
    tmux split-window -v -t autonomous
    tmux split-window -h -t autonomous:os.0

    #run boot os for all device:
    tmux send-keys -t autonomous:os.0 'cd $HOME/aos/system && python setup.py' C-m

    #run box control desk
    tmux send-keys -t autonomous:os.1 'cd $HOME/aos/system/$DEVICE_TYPE/deskApp/deskRep && bash run.sh' C-m

fi
