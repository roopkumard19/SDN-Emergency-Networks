#!/bin/sh

cd ~/wmSDN/openvswitch
./configure --with-linux=/lib/modules/`uname -r`/build
make
rmmod openvswitch
insmod ./datapath/linux/openvswitch.ko
# Once you verify that the kernel modules load properly, you should
#   install them:
make modules_install
cd  ~/ns-allinone-3.17/ns-3.17
sudo ./waf shell
sh cored
#`./run-wmsdn-2.sh
