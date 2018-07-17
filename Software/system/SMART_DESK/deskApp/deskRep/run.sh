#!/usr/bin/env bash
#add current path to PATH
export PATH=$PATH:$PWD
# Detect Serial device files
# 
dataFile="data.dat"
os="none"
device=NULL
#Detect which board to run
if  uname -m  | grep x86_64  ; then
	if [ -e "/dev/ttyUSB0" ] ; then
		device="/dev/ttyUSB0"
        	sudo chmod 777 $device
        	echo "detect /dev/ttyUSB0"
	fi
	os="x64"
fi

if uname -m |grep arm ; then
	if [ -e "/dev/ttyS0" ] ; then
			device="/dev/ttyS0"

        	sudo chmod 777 $device
        	sudo chmod a+rw /sys/class/backlight/rpi_backlight/bl_power
        	sudo chmod a+rw /sys/class/backlight/rpi_backlight/brightness
        	echo "Detected /dev/ttyS0"
	fi
	os="RPI"
	echo "use device $device"
	echo "Detected Arm Board"
fi
# Check if the data.mat file is exist.
if [ -f "$dataFile" ] ; then
#Detct the Control Box type in data.mat	
	if  grep -q "Timotion" "data.dat" 
	#Timotion Control Box Detected
	then
		echo "Selected Timotion Box"
		if [ -f "Timotion/user/$os/deskrep" ] ; then
		    if [ "$device" != NULL ] ; then
			sudo chmod +x  Timotion/user/$os/deskrep
			if  ps -ax |grep deskrep | grep -v grep  ; then
				echo "App is runnig"
			else
				./Timotion/user/$os/deskrep $device
			fi
		    else
			echo "Device is not connected"
		    fi
		else
			echo "/Timotion/user/$os/deskrep not found "
		fi
	else
		if grep -q "Jiecang" "data.dat"
		#Jiecang Box control Box detected
		then
			echo "Selected Jiecang Box"
			if [ -f "Jiecang/user/$os/deskrep" ]  ; then
			    if [ "$device"  != NULL ] ; then
				sudo chmod +x Jiecang/user/$os/deskrep
				if ps -ax |grep deskrep | grep -v grep  ; then
					echo "App is runnig"
				else
					./Jiecang/user/$os/deskrep $device
				fi
			    else
				echo "Device is not connected"
			    fi
				
			else
				echo "/Jiecang/user/$os/deskrep not found or device not connected"
			fi
		else
			if grep -q "AddonBoard" "data.dat"
			# AddonBoard Controller Detected
			then
				echo "selected AddonBoard"
				if [ -f "AddonBoard/user/$os/deskrep" ]  ; then
				    if [ "$device" != NULL ] ; then
					sudo chmod +x AddonBoard/user/$os/deskrep
					if ps -ax |grep deskrep | grep -v grep  ; then
						echo "App is runnig"
					else
						./AddonBoard/user/$os/deskrep $device
					fi
				    else
					echo "Device is not connected"
				    fi
				else
					echo "/AddonBoard/user/$os/deskrep not found or device not connected"
				fi
			fi
		fi
	fi
else
	echo "$dataFile not Found"
fi
