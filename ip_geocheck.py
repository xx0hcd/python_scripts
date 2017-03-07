#!/usr/bin/python
#./ip_geocheck.py
#Usage: Prompts for IP addres, checks against freegeoip.net, displays results in json
#xx0hcd
#Needs requests library installed

import requests

def main():

    while True:

        try:

            IP = raw_input("Enter IP Address: ")

            URL = "http://freegeoip.net/json/"

            REQ = URL + IP

            r = requests.get(REQ)

            output = r.json()

            print output

            break

        except ValueError:
            print "[-] "
            print "[-] Error Processing Request. Check IP address format. "
	    print "[-] "


if __name__ == "__main__":
    while True:
        try:
            main()
	    break

        except IOError:
            print "[-] "
            print "[-] Error Processing Request. Check IP address format. "
	    print "[-] "
            break
