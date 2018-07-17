#!/bin/bash

#check new system:
export FIRMWARE_UPDATE__TMP_PATH=$HOME/aos/tmp/system
export TARGET_UPDATE_PATH=$HOME/aos/
export SYSTEM=$TARGET_UPDATE_PATH/system/$DEVICE_TYPE/system.sh

#if [ -d "$FIRMWARE_UPDATE__TMP_PATH" ]; then
#    mv --backup=numbered $FIRMWARE_UPDATE__TMP_PATH $TARGET_UPDATE_PATH
#    sleep 3
#fi
cd $HOME/aos/ability/firmware_update/ && python check_update.py
bash $SYSTEM
