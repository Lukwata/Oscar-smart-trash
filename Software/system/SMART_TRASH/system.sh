#!/bin/bash

# load apps at startup by default
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib/
#xinput --set-prop 'FT5406 memory based driver' 'Coordinate Transformation Matrix' 0 1 0 -1 0 1 0 0 1
#sleep 2
tmux has-session -t brain
if [ $? != 0 ]; then

    tmux new -s brain -n brain -d
    tmux split-window -h -t brain
    tmux send-keys -t brain:brain.0 'cd $HOME/aos/ && ulimit -s 1024 && ulimit -r 0 && chmod +x system/SMART_TRASH/brain && system/SMART_TRASH/brain -b $HOME/aos/data/pr_device.json' C-m
    #sleep 10
    tmux send-keys -t brain:brain.1 'cd $HOME/testSmartTrashV2/trashcanApp && sh ./run.sh' C-m
   
   
fi
