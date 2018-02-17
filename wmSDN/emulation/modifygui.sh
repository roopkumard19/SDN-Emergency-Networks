#!/bin/bash


#./modifygui.sh {Failed node number} {Drone_node__start_id} {Drone_node__end_id}
# example: 
# ./modifygui.sh 2 10 13

#coresendmsg link n1number=3 n2number=9 guiattr='color=black'
#coresendmsg link n1number=1 n2number=8 guiattr='color=black'
#coresendmsg link n1number=6 n2number=$1 guiattr='color=black'
#coresendmsg link n1number=7 n2number=$1 guiattr='color=black'
#coresendmsg link n1number=5 n2number=$1 guiattr='color=black'

if [ $# -lt 3 ]
then
    echo "Arguments missing"
    echo "./modifygui.sh {Failed node number} {Drone_node__start_id} {Drone_node__end_id}"
    echo "example:"
    echo "./modifygui.sh 2 10 13"
    exit 1
fi

START=$2
END=$3


for (( c=$START; c<=$END; c++ ))
do
	coresendmsg node number=$c icon=/usr/lib/core/icons/normal/drone.gif
done

sleep 12
coresendmsg node number=$1 icon=/usr/lib/core/icons/normal/router_red.gif
sleep 3

coresendmsg node number=15 name='n15' xpos=770 ypos=613
sleep 1
coresendmsg node number=15 name='n15' xpos=701 ypos=570
sleep 1
coresendmsg node number=15 name='n15' xpos=636 ypos=544
sleep 1
coresendmsg node number=15 name='n15' xpos=575 ypos=515
sleep 1
coresendmsg node number=15 name='n15' xpos=520 ypos=491
sleep 1
coresendmsg node number=15 name='n15' xpos=471 ypos=465
sleep 1
coresendmsg node number=15 name='n15' xpos=424 ypos=440
sleep 1
coresendmsg node number=15 name='n15' xpos=370 ypos=416
sleep 1
coresendmsg node number=15 name='n15' xpos=304 ypos=408
sleep 1
coresendmsg node number=15 name='n15' xpos=267 ypos=395
sleep 1
coresendmsg node number=15 name='n15' xpos=222 ypos=381
coresendmsg node flags=del number=2 name='n2'
#source /home/user/wmSDN/emulation/bashrc
#corevcmd n$2 killall olsrd
#corevcmd n$2 ip link set eth0 down
#corevcmd n$2 ip link set eth1 down
#echo $(date -u) "n$2 down"




sleep 5
coresendmsg node number=6 icon=/usr/lib/core/icons/normal/router_red.gif
sleep 3

coresendmsg node number=17 name='n17' xpos=855 ypos=590
sleep 1
coresendmsg node number=17 name='n17' xpos=910 ypos=540
sleep 1
coresendmsg node number=17 name='n17' xpos=960 ypos=500
sleep 1
coresendmsg node number=17 name='n17' xpos=1010 ypos=460
sleep 1
coresendmsg node number=17 name='n17' xpos=1070 ypos=420
sleep 1
coresendmsg node number=17 name='n17' xpos=1120 ypos=360
sleep 1
coresendmsg node number=17 name='n17' xpos=1170 ypos=330
sleep 1
coresendmsg node number=17 name='n17' xpos=1220 ypos=285
sleep 1
coresendmsg node number=17 name='n17' xpos=1280 ypos=240
sleep 1

coresendmsg node number=17 name='n17' xpos=1324 ypos=207
coresendmsg node flags=del number=6 name='n6'