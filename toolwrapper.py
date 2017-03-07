#!/usr/bin/python

#./toolwrapper.py - xx0hcd
#Tool to scan multiple hosts from a list (mostly for if the tool doesn't support multiple hosts :))
#Tool must already be installed!
#If tool has arguments, enclose in quotes. i.e. './toolwrapper.py -t 'nbtscan -r' -f target_file.txt'
#If the tool supports writing use it in the quotes, if not for now redirect to stdout via '>' etc.

import os
import sys
import getopt



def cmds(argv):
	while True:
		try:
			f = open(hostfile, "rb")
			list = f.readlines()
			f.close()
			break
		except ValueError:
			print "Error with file, I should probably write something that checks if the file exists and append a number to the end of the file name or something... "


	for word in list:
		cmd = tool + ' ' + word
		os.system(cmd)



def main(argv):
	global tool
	global hostfile

	tool = ''
	hostfile = ''

	try:
		opts, args = getopt.getopt(argv, "ht:f:",["tool=","hostfile="])
	except getopt.GetoptError:
		print "[-] "
		print "[-] "
		print "[+] "
		print "[+] -t, --tool	Name of tool with arguements to use. "
		print "[+] "
		print "[+] -f, --hostfile  	Name of taget host file to use. "
		print "[+] "
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print "[+] "
			print "[+] Help Options: "
			print "[+] "
			print "[+] -t, --tool	Name of tool to run. "
			print "[+] 		Enclose command and argument with quotes. "
			print "[+] 		i.e. './toolwrapper.py -t 'nbtscan -r' -f target_hostfile.txt'"
			print "[+] "
			print "[+] -f, --hostfile	Name of file that conatins targets. "
			print "[+] "
			print "[+] Example: ./toolwrapper.py -t 'ping -c 1' -f targetlist.txt. "
			print "[+] "
			print "[+] Example: ./toolwrapper.py -t 'snmp-check' -f targetlist.txt. "
			print "[+] "
			sys.exit()
		elif opt in ("-t, --tool"):
			tool = arg
		elif opt in ("-f, --hostfile"):
			hostfile = arg

if __name__ == "__main__":
	while True:
		try:
			main(sys.argv[1:])
			cmds(sys.argv[1:])
			break
		except IOError, e:
			print "[-] "
			print "[-] Invalid Options: "
			print "[-] "
			print "[+] -t, --tool	Name of tool to run. "
			print "[+] 		Enclose command and argument with quotes. "
			print "[+] "
			print "[+] -f, --hostfile	Name of file that conatins targets. "
			print "[+] "
			print "[+] Example: ./toolwrapper.py -t 'ping -c 1' -f targetlist.txt. "
			print "[+] "
			print "[+] Example: ./toolwrapper.py -t 'snmp-check' -f targetlist.txt. "
			print "[+] "
			break	


