#!/usr/bin/env bash
#add current path to PATH
export PATH=$PATH:$PWD
# Detect Serial device files
a=$(ls /dev/ttyS* |grep ttyS0)
if [ "$a" = "/dev/ttyS0" ] ; then
	sudo chmod 777 /dev/ttyS0
	echo "Detected /dev/ttyS0"
fi

a=$(ls /dev/serial* | grep serial0)
if [ "$a" = "/dev/serial0" ] ; then
	sudo chmod 777 /dev/serial0
	echo "Detected /dev/serial0"
fi

a=$(ls /dev/ttyUSB* | grep USB0)
if [ "$a" = "/dev/ttyUSB0" ] ; then
	sudo chmod 777 /dev/ttyUSB0
	echo "detect /dev/ttyUSB0"
fi
# 
dataFile="data.dat"
os="none"
#Detect which board to run
if uname -m |grep x86_64 ; then
	os="x64"
	device="/dev/ttyUSB0"
	echo "use device $device"
	echo "Detected $os "
fi

if uname -m |grep arm ; then
	os="RPI"
	device="/dev/ttyS0"
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
		if [ -f "TimotionV1/user/$os/deskrep" ] ; then
			sudo chmod +x  TimotionV1/user/$os/deskrep
			./TimotionV1/user/$os/deskrep $device
		else
			echo "/TimotionV1/user/$os/deskrep not found "
		fi
	else
		if grep -q "Jiecang" "data.dat"
		#Jiecang Box control Box detected
		then
			echo "Selected Jiecang Box"
			if [ -f "Jiecang/user/$os/deskrep" ] ; then
				sudo chmod +x Jiecang/user/$os/deskrep
				./Jiecang/user/$os/deskrep $device
			else
				echo "/Jiecang/user/$os/deskrep not found"
			fi
		else
			if grep -q "AddonBoard" "data.dat"
			# AddonBoard Controller Detected
			then
				echo "selected AddonBoard"
				if [ -f "AddonBoard/user/$os/deskrep" ] ; then
					sudo chmod +x AddonBoard/user/$os/deskrep
					./AddonBoard/user/$os/deskrep $device
				else
					echo "/AddonBoard/user/$os/deskrep not found"
				fi
			fi
		fi
	fi
else
	echo "$dataFile not Found"
fi
