#! /bin/sh
#sed -i "s/__SSID__/\"$1\"/g" wpa_supplicant.conf
#sed -i "s/__PASS_WORD__/\"$2\"/g" wpa_supplicant.conf

# raspi-wifi-blindscript v4
#   A minimium command line script to configure Wi-Fi network on Raspbian 
#   system for Raspberry Pi(R) ARM computer. 
# Project HP: https://github.com/shamiao/raspi-wifi-blindscript
#
# Copyright (C) 2013 Sha Miao
# This program is released under the MIT license, see LICENSE file or 
# <http://opensource.org/licenses/MIT> for full text.
#
# See README for usage. 

###############################################################
#################### PLEASE EDIT THIS PART ####################
###############################################################

# SSID (aka. network name).
SSID=$1
# Network password. (WPA-PSK/WPA2-PSK password, or WEP key)
PASSWORD=$2 # 'network_password_goes_here'

# Network encryption method.
# * 'WPA' for WPA-PSK/WPA2-PSK (note: most Wi-Fi networks use WPA);
# * 'WEP' for WEP;
# * 'Open' for open network (aka. no password).
ENCRYPTION='WPA'
if [ -z "$PASSWORD" ] ; then
   ENCRYPTION='Open' 
fi 
echo "Config type : $ENCRYPTION"

###############################################################
####################   OK. STOP EDITING!   ####################
###############################################################

if [ $(id -u) -ne 0 ]; then
  printf "This script must be run as root. \n"
  exit 1
fi
#remove old_network first.
wpa_cli remove_network 0
wpa_cli remove_network 1
wpa_cli remove_network 2
wpa_cli remove_network 3
wpa_cli save_config

#remove old_network first.
NETID=$(wpa_cli add_network | tail -n 1)
echo "CONFIG FOR NETWORK ID: $NETID"
wpa_cli set_network $NETID ssid \"$SSID\"
case $ENCRYPTION in
'WPA')
    wpa_cli set_network $NETID key_mgmt WPA-PSK
    wpa_cli set_network $NETID psk \"$PASSWORD\"
    ;;
'WEP')
    wpa_cli set_network $NETID wep_key0 $PASSWORD
    wpa_cli set_network $NETID wep_key1 $PASSWORD
    wpa_cli set_network $NETID wep_key2 $PASSWORD
    wpa_cli set_network $NETID wep_key3 $PASSWORD
    ;;
'Open')
    wpa_cli set_network $NETID key_mgmt NONE
    ;;
*)
    ;;
esac
wpa_cli enable_network $NETID
wpa_cli save_config
wpa_cli select_network $NETID
#sudo service dhcpcd restart 
