#!/usr/bin/python

##Uncomment this if you want to randomize ports in the list..
#import random

##Just using to keep track of attempts in print statements.
count = 0
 
from scapy.all import *
conf.verb = 0

##The List of ports to try in order...
ports = [1, 2, 3]

##... or uncomment this to randomize ports in your list.
#random.shuffle(ports)

for dport in range(0, len(ports)):
 
    ##Just using to keep track of attempts in print statements.
    count = count+1
    ##Destination IP   
    ip = IP(dst="192.168.34.133")
    ##Source port you want to use
    port = 35001
    SYN = ip/TCP(sport=port, dport=ports[dport], flags="S", window=2048, options=[('MSS',1460)], seq=0)
    send(SYN) ; print "Knock ---> #", count

    ##Add more lines here if you want to hit the list multiple times. i.e. 1,1,2,2,3,3,etc.
    
print '-------------'
print '-------------'
print 'Start nmap  :'
print '-------------'
print '-------------'
subprocess.call("nmap -sV -T4 192.168.34.133", shell=True)
print '-------------'
print '-------------'
print 'Finish nmap :'
print '-------------'
print '-------------'
