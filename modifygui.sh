#!/bin/bash


# Move these 4 lines in python script, And attach drones to wlan1, get ip and mac addresess for them
coresendmsg node flags=add number=12 type=0 name='n12' xpos=860 ypos=650 icon=/usr/lib/core/icons/normal/drone.gif
coresendmsg node flags=add number=13 type=0 name='n13' xpos=906 ypos=650
coresendmsg node flags=add number=14 type=0 name='n14' xpos=842 ypos=600
coresendmsg node flags=add number=15 type=0 name='n15' xpos=891 ypos=604

coresendmsg link n1number=3 n2number=9 guiattr='color=black'
coresendmsg link n1number=1 n2number=8 guiattr='color=black'
coresendmsg link n1number=6 n2number=$1 guiattr='color=black'
coresendmsg link n1number=7 n2number=$1 guiattr='color=black'
coresendmsg link n1number=5 n2number=$1 guiattr='color=black'

sleep 10
coresendmsg node number=$2 icon=/usr/lib/core/icons/normal/router_red.gif
sleep 3
coresendmsg node number=12 name='n12' xpos=770 ypos=613
sleep 1
coresendmsg node number=12 name='n12' xpos=701 ypos=570
sleep 1
coresendmsg node number=12 name='n12' xpos=636 ypos=544
sleep 1
coresendmsg node number=12 name='n12' xpos=575 ypos=515
sleep 1
coresendmsg node number=12 name='n12' xpos=520 ypos=491
sleep 1
coresendmsg node number=12 name='n12' xpos=471 ypos=465
sleep 1
coresendmsg node number=12 name='n12' xpos=424 ypos=440
sleep 1
coresendmsg node number=12 name='n12' xpos=370 ypos=416
sleep 1
coresendmsg node number=12 name='n12' xpos=304 ypos=366
sleep 1
coresendmsg node number=12 name='n12' xpos=257 ypos=342
coresendmsg node flags=del number=2 name='n2'
sleep 1
coresendmsg node number=12 name='n12' xpos=200 ypos=300

#source /home/user/wmSDN/emulation/bashrc
#corevcmd n$2 killall olsrd
#corevcmd n$2 ip link set eth0 down
#corevcmd n$2 ip link set eth1 down
#echo $(date -u) "n$2 down"

