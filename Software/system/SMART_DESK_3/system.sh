#!/bin/bash

# load apps at startup by default
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib/
xinput --set-prop 'FT5406 memory based driver' 'Coordinate Transformation Matrix' 0 1 0 -1 0 1 0 0 1
sleep 2
tmux has-session -t brain
if [ $? != 0 ]; then

    tmux new -s brain -n brain -d
    tmux send-keys -t brain:brain 'cd $HOME/aos/ && ulimit -s 1024 && ulimit -r 0 && chmod +x system/SMART_DESK_3/brain && system/SMART_DESK_3/brain -b $HOME/aos/data/pr_device.json' C-m

fi