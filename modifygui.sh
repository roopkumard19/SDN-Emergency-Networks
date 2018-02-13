#!/bin/bash


#./modifygui.sh {Failed node number} {Drone_node__start_id} {Drone_node__end_id}
# example: 
# ./modifygui.sh 2 10 13

#coresendmsg link n1number=3 n2number=9 guiattr='color=black'
#coresendmsg link n1number=1 n2number=8 guiattr='color=black'
#coresendmsg link n1number=6 n2number=$1 guiattr='color=black'
#coresendmsg link n1number=7 n2number=$1 guiattr='color=black'
#coresendmsg link n1number=5 n2number=$1 guiattr='color=black'

sleep 10

START=$2
END=$3


for (( c=$START; c<=$END; c++ ))
do
	coresendmsg node number=$c icon=/usr/lib/core/icons/normal/drone.gif
done

coresendmsg node number=$1 icon=/usr/lib/core/icons/normal/router_red.gif
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

