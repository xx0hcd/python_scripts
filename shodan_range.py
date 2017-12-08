#!/usr/bin/python
#shodan_range.py
#python shodan_range.py -r <IP CIDR range> -f </path/output_filename>
#xx0hcd
#tested on kali2 - written becasue of issues with rate limiting and API limitations using 'api.host'

import time
import os
import getopt
import sys

try:
	import shodan
except:
	print "Please run 'pip install shodan' or 'easy_install -U shodan' to install shodan library."

errors = """
[-]
[-] The IP range to scan and output filename are required.
[-]
[+]
[+] -r, --range 	Enter IP CIDR range.
[+]
[+] -f, --filename	Enter path/filename for output file.
[+]
[+] i.e. python shodan_range.py -r 72.163.1.0/24 -f /tmp/outfile.txt
[+]
"""

if len(sys.argv) <= 1:
	print errors
	exit(1)

def search(argv):

	try:
			#making sure the IP range temp file is not there from a previous run, etc.
			if os.path.exists("/tmp/1out.txt"):
				os.system("rm -r /tmp/1out.txt")			

	except (OSError,IOError):
		print "[-] "
		print "[-] Problem deleting temp file. Check file permissions. "
		print "[-] "
	
	try:
		#getting the IP range into a list in a temp file
		query = 'net:' + ip_range

		results = api.search(query)
	
		for service in results['matches']:
			
			try:
				with open("/tmp/1out.txt", "a+") as file1:
					file1.seek(0)
					print >> file1, service['ip_str']
					
			except shodan.APIError, e:
				print "Error: %s" % e

	except shodan.APIError, e:
		print "Error: %s" % e


def hosts():
	
	while True:

		try:
			#api.host() gave me errors when attempting to pull info from a CIDR range. Looping through a list as a work around..
			with open("/tmp/1out.txt", "r") as f:

				for line in f:
					
					host = api.host(line)
					host_file1 = open("/tmp/host_output.txt", "a+")
					host_file1.seek(0)

					print >> host_file1, """
IP: %s
Organization: %s
Operating System: %s
""" % (host['ip_str'], host.get('org', 'n/a'), host.get('os', 'n/a'))

					#'data' has a lot of fields you can get info from, this is using the example in the API docs.
					for item in host['data']:
       						print >> host_file1, """
Port: %s
Banner:
%s

              """ % (item['port'], item['data'])
					#Two second delay worked during testing, get rate limiting errors otherwise.
					time.sleep(2)					

		except shodan.APIError, e:
			print "Error: %s" % e

		break

def cleanup(argv):

	while True:	
		#making sure IP range temp file is removed after processing
		try:
			if os.path.exists("/tmp/1out.txt"):
				os.system("rm -r /tmp/1out.txt")			

		except (OSError,IOError):
			print "[-] "
			print "[-] Problem deleting temp file. Check file permissions. "
			print "[-] "
		#making sure host temp file is removed and replaced with user defined location
		try:
			if os.path.exists("/tmp/host_output.txt"):
				os.rename("/tmp/host_output.txt", filename)
				print "[+] "
				print "[+] Output file located at ", filename
				print "[+] "

		except (OSError,IOError):
			print "[-] "
			print "[-] Problem moving file. File is temporarily  stored at /tmp/host_output.txt. "
			print "[-] "
			
		break

def main(argv):
	
	global ip_range
	global filename
	global api

	#Your Shodan API key goes here.
	api_key = "<API_key_goes_here>"
	api = shodan.Shodan(api_key)

	try:
		opts, args = getopt.getopt(argv, "hr:f:",["ip_range=","filename="])

	except getopt.GetoptError:
		print errors
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-h':
			print errors
			sys.exit()
		elif opt in ("-r", "--ip_range"):
			ip_range = arg
		elif opt in ("-f", "--filename"):
			filename = arg
	
	try:
		if os.path.exists(filename):
			print "[+] "
			print "[+] File: " + filename + " already exists! Please remove the old file or type in a new path/filename. "
			print "[+] "
			sys.exit()
	except (OSError, IOError):
		print "[-] "
		print "[-] Problem writing to ", filename
		print "[-] "

if __name__ == "__main__":

	while True:
		try:
			main(sys.argv[1:])
			search(sys.argv[1:])
			hosts()
			cleanup(sys.argv[1:])
			break

		except IOError:
			print errors
			break

		except KeyboardInterrupt:
			print ""
			print "[+] "
			print "[+] Ctrl ^C, Aborted by user. "
			print "[+] "
			sys.exit(3)
