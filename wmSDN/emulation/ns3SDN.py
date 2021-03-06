#!/usr/bin/python -i
# vim:ts=2:expandtab:shiftwidth=2
#
#  Copyright 2013 Claudio Pisa, Andrea Detti
#
#  This file is part of wmSDN
#
#  wmSDN is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  wmSDN is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with wmSDN.  If not, see <http://www.gnu.org/licenses/>.
#

'''
ns3wifi.py - This script demonstrates using CORE with the ns-3 Wifi model.

How to run this:

pushd ~/ns-allinone-3.16/ns-3.16
sudo ./waf shell
popd
python -i ns3wifi.py

To run with the CORE GUI:

pushd ~/ns-allinone-3.16/ns-3.16
sudo ./waf shell
cored

# in another terminal
cored -e ./ns3wifi.py
# in a third terminal
core
# now select the running session

'''
import subprocess
import os, sys, time, optparse, datetime, math, socket
try:
    from core import pycore 
except ImportError:
    # hack for Fedora autoconf that uses the following pythondir:
    if "/usr/lib/python2.6/site-packages" in sys.path:
        sys.path.append("/usr/local/lib/python2.6/site-packages")
    if "/usr/lib64/python2.6/site-packages" in sys.path:
        sys.path.append("/usr/local/lib64/python2.6/site-packages")
    if "/usr/lib/python2.7/site-packages" in sys.path:
        sys.path.append("/usr/local/lib/python2.7/site-packages")
    if "/usr/lib64/python2.7/site-packages" in sys.path:
        sys.path.append("/usr/local/lib64/python2.7/site-packages")
    from core import pycore

import ns.core
from core.sdt import Sdt
from core.misc import ipaddr 
from core.misc.ipaddr import MacAddr
from corens3.obj import Ns3Session, Ns3WifiNet, CoreNs3Net

import sys
sys.path.insert(0, '/home/user/wmSDN/controller')

from olsr_parser import *
#sys.path.append(os.getcwd())
#import coreconf

# python interactive shell tab autocompletion
import rlcompleter, readline
readline.parse_and_bind('tab:complete')


custom_services_dir = '/home/user/wmSDN/emulation/core_services'
openvswitch_dir = '/home/user/wmSDN/openvswitch'
olsr_dir = '/home/user/wmSDN/olsrd'
olsrd_dir = '/home/user/wmSDN/olsrd'
scripts_dir = '/home/user/wmSDN/scripts'

N = 0
G = 0
D = 0
nX = []
nY = []
gX = []
gY = []
dX = []
dY = []

mesh_location = []
def parse_input(file):
    global N
    global G
    global D
    global nX
    global nY
    global gX
    global gY
    global dX
    global dY

    with open(file,'r') as f:
        #n = int(f.readline())
        N = int(f.readline().rstrip())
        for i in range(0,N):
            temp = f.readline().rstrip().split(',')
            nX.append(int(temp[0]))
            nY.append(int(temp[1]))
        G = int(f.readline().rstrip())
        for i in range(0,G):
            temp = f.readline().rstrip().split(',')
            gX.append(int(temp[0]))
            gY.append(int(temp[1]))
        D = int(f.readline().rstrip())
        for i in range(0,D):
            temp = f.readline().rstrip().split(',')
            dX.append(int(temp[0]))
            dY.append(int(temp[1]))
        print "Nodes:",N
        print "Gateways:",G
        print nX,nY,gX,gY,dX,dY
        print "Drones:",D

def add_to_server(session):
    ''' Add this session to the server's list if this script is executed from
    the cored server.
    '''
    global server
    try:
        server.addsession(session)
        return True
    except NameError:
        return False

def wifisession(opt):
    ''' Run a test wifi session.
    '''
    #myservice = "Olsrd4Service"
    global N
    global G
    global D
    global nX
    global nY
    global gX
    global gY
    global dX
    global dY

    myservice = "OpenvswitchService"
    #myservice = "OpenflowService"
    numWirelessNode=(G+N)
    numWiredNode=5
    ns.core.Config.SetDefault("ns3::WifiMacQueue::MaxPacketNumber",ns.core.UintegerValue(100)) 
    session = Ns3Session(persistent=True, duration=opt.duration)
    session.cfg['openvswitch_dir'] = openvswitch_dir #coreconf
    session.cfg['olsr_dir'] = olsr_dir #coreconf
    session.cfg['olsrd_dir'] = olsrd_dir #coreconf
    session.name = "ns3SDN"
    session.filename = session.name + ".py"
    session.node_count = str(numWirelessNode + numWiredNode + 1)
    session.services.importcustom(custom_services_dir) #coreconf
    add_to_server(session)

    wifi1 = session.addobj(cls=Ns3WifiNet, name="wlan1", rate="OfdmRate54Mbps")
    wifi2 = session.addobj(cls=Ns3WifiNet, name="wlan2", rate="OfdmRate54Mbps")
    #wifi.wifi.SetStandard(ns.wifi.WIFI_PHY_STANDARD_80211b)
    #wifi.wifi.SetRemoteStationManager("ns3::ConstantRateWifiManager", "DataMode",ns.core.StringValue("DsssRate11Mbps"), "NonUnicastMode", ns.core.StringValue("DsssRate11Mbps"))
    wifi1.setposition(30, 30, 0)
    wifi1.phy.Set("RxGain", ns.core.DoubleValue(20.0))
    wifi2.setposition(1668, 34, 0)
    wifi2.phy.Set("RxGain", ns.core.DoubleValue(20.0))
    prefix = ipaddr.IPv4Prefix("10.0.0.0/16")

    hub1 = session.addobj(cls=pycore.nodes.HubNode, name="hub1")
    hub1.setposition(747,300,0)
    ptp1 = session.addobj(cls=pycore.nodes.PtpNet, name="ptp1") 
    ptp2 = session.addobj(cls=pycore.nodes.PtpNet, name="ptp2") #controller1 network
    ptp3 = session.addobj(cls=pycore.nodes.PtpNet, name="ptp3") #controller2 network
    hub_ID = hub1.objid
    nodes = []
    drones = []
    def ourmacaddress(n):
        return MacAddr.fromstring("02:02:00:00:00:%02x" % n)

    for i in xrange(1, N+1):
        print "Adding node:",i
        node = session.addnode(name = "n%d" % i)
        if i <= 4:
            node.newnetif(wifi1, ["%s/%s" % (prefix.addr(i), prefix.prefixlen)], hwaddr=ourmacaddress(i))
        else:
             node.newnetif(wifi2, ["%s/%s" % (prefix.addr(i), prefix.prefixlen)], hwaddr=ourmacaddress(i))
        if i == 1:
            node.newnetif(ptp1,["192.168.1.2/24"])    
        if i == 3: #the wireless node which is attached to the controller
            node.newnetif(ptp2,["10.100.100.2/24"])
        if i == 8:
            node.newnetif(ptp3,["10.100.100.2/24"])
        session.services.addservicestonode(node,"router",myservice,verbose=True)
        session.services.bootnodeservices(node)
        nodes.append(node)

    for i in xrange(N+1, numWirelessNode + 1):
        print "Adding gateway:",i
        node = session.addnode(name = "gw%d" % i)
        if i == 12:
            node.newnetif(wifi2, ["%s/%s" % (prefix.addr(i), prefix.prefixlen)], hwaddr=ourmacaddress(i))
        else:
            node.newnetif(wifi1, ["%s/%s" % (prefix.addr(i), prefix.prefixlen)], hwaddr=ourmacaddress(i))

        node.newnetif(hub1,["192.168.200.%d/24" % i])
        session.services.addservicestonode(node,"router",myservice,verbose=True)
        session.services.bootnodeservices(node)
        nodes.append(node)

    node = session.addnode(name = "controller1")
    node.newnetif(ptp2,["10.100.100.100/24"])
    nodes.append(node)

    node = session.addnode(name = "controller2")
    node.newnetif(ptp3,["10.100.100.100/24"])
    nodes.append(node)


    for i in xrange(len(nodes)+1, len(nodes)+D+1):
        print "Adding drone:",i
        node = session.addnode(name = "d%d" % i)
        if i <=16:
            node.newnetif(wifi1, ["%s/%s" % (prefix.addr(i), prefix.prefixlen)], hwaddr=ourmacaddress(i))  
        else:
            node.newnetif(wifi2, ["%s/%s" % (prefix.addr(i), prefix.prefixlen)], hwaddr=ourmacaddress(i))  
        session.services.addservicestonode(node,"router",myservice,verbose=True)
        session.services.bootnodeservices(node)
        drones.append(node)

    session.setupconstantmobility()

    n_ind = 0
    for i in xrange(1, N+1):
        print "setting position for nodes[i]",i
        nodes[n_ind].setns3position(nX[n_ind],nY[n_ind],0)
        nodes[n_ind].setposition(nX[n_ind],nY[n_ind],0)
        n_ind = n_ind + 1
    
    g_ind = 0
    for i in xrange(N+1, numWirelessNode + 1):
        print "setting position for nodes[i]",i
        nodes[N + g_ind].setns3position(gX[g_ind],gY[g_ind],0)
        nodes[N + g_ind].setposition(gX[g_ind],gY[g_ind],0)
        g_ind = g_ind + 1
    
    for i in xrange(0, D):
        print "setting position for drones[i]",i
        drones[i].setns3position(dX[i],dY[i],0)
        drones[i].setposition(dX[i],dY[i],0)

    nodes[len(nodes)-2].setns3position(257,119,0)
    nodes[len(nodes)-2].setposition(257,119,0)
    
    nodes[len(nodes)-1].setns3position(1466,200,0)
    nodes[len(nodes)-1].setposition(1466,200,0)
    #wifi.usecorepositions()
    # PHY tracing
    #wifi.phy.EnableAsciiAll("ns3wifi")


    session.thread = session.run(vis=False)

    #session.connect(session.objbyname(session.name))
    #print "session_ID:",session.sessionid
    #print session.master
    #subprocess.call(['./modifygui.sh' '2','10','13'])

    #os.system("/home/user/wmSDN/emulation/modifygui.sh 2 15 18")
    #nodes[0].icmd(["sh", "./olsrdservice_start.sh", "start"])
    return session

def main():
    parse_input('/home/user/wmSDN/emulation/input.txt')
    ''' Main routine when running from command-line.
    '''
    usagestr = "usage: %prog [-h] [options] [args]"
    parser = optparse.OptionParser(usage = usagestr)
    parser.set_defaults(duration = 600, verbose = False)

    parser.add_option("-d", "--duration", dest = "duration", type = int,
      help = "number of seconds to run the simulation")
    parser.add_option("-v", "--verbose", dest = "verbose",
      action = "store_true", help = "be more verbose")

    def usage(msg = None, err = 0):
        sys.stdout.write("\n")
        if msg:
            sys.stdout.write(msg + "\n\n")
        parser.print_help()
        sys.exit(err)

    (opt, args) = parser.parse_args()


    for a in args:
        sys.stderr.write("ignoring command line argument: '%s'\n" % a)

    return wifisession(opt)


if __name__ == "__main__" or __name__ == "__builtin__":
    session = main()
    print "\nsession =", session

