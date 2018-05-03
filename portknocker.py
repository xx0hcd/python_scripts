#!/usr/bin/python

##Uncomment this and 'random.shuffle(ports)' if you want to randomize ports in the list.
#import random

counts = 0

ipaddr = raw_input("Enter destination IP address: ")

from scapy.all import *
conf.verb = 0

port_in = raw_input("Enter ports to use comma separated. (i.e. 7000,666,8890) : ")
ports = [int(i) for i in port_in.split(',')]
print "Knocking with ports :", ports, "on host ", ipaddr

#uncomment this and 'import random' to randomize ports in the list.
#random.shuffle(ports)

for dport in range(0, len(ports)):
    count = counts+1
    ip = IP(dst=ipaddr)
    ##Source port you want to use
    port = 35001
    SYN = ip/TCP(sport=port, dport=ports[dport], flags="S", window=2048, options=[('MSS',1460)], seq=0)
    send(SYN)

for x in ports:
    print '------------------------------------------'
    print "Knock ---> port#", x

  
print '------------------------------------------'
print '------------------------------------------'
print 'Running nmap to check for new open ports: '
print '------------------------------------------'
print '------------------------------------------'
#run nmap to check what new ports are open.
nvar = "nmap -p- -T4 --reason " + ipaddr
subprocess.call(nvar, shell=True)
print '------------------------------------------'
print '------------------------------------------'
print 'Finished running nmap. '
print '------------------------------------------'
print '-----------------------'
