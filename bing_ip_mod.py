#!/usr/bin/python3
#bing_ip_mod.py
#python3 bing_ip_mod.py -r 72.163.1.0/24 -f /tmp/bing_out.txt
#written to use the Bing search IP modifier to get lists of hostnames behind single IP/load balancer, etc.
#xx0hcd

import ipaddress
import http.client, urllib.parse, json
import sys, os, time
import getopt


errors = ("""
[-]
[-] The IP range to scan and output filename are required.
[-]
[+]
[+] -r, --range 	Enter IP CIDR range.
[+]
[+] -f, --filename	Enter path/filename for output file.
[+]
[+] i.e. python3 bing_ip_mod.py -r 72.163.1.0/24 -f /tmp/outfile.txt
[+]
""")

if len(sys.argv) <= 1:
    print (errors)
    exit(1)

def search(argv):
    
    ip = ipaddress.ip_network(ip_range)

    try:
    #making sure the IP temp file is not there from a previous run, etc.
        if os.path.exists("/tmp/bing_hosts.txt"):
            os.system("rm -r /tmp/bing_hosts.txt")			

    except (OSError,IOError):
        print ("[-] ")
        print ("[-] Problem deleting temp file. Check file permissions. ")
        print ("[-] ")

    #put the CIDR range into a list in a temp file
    try:

        with open("/tmp/bing_hosts.txt", "a+") as f:
            for i in ip.hosts():
                print(i, "\n", end="", file=f)
            f.close()
            time.sleep(1)

    except (OSError, IOError):
        print("[-] ")
        print("[-] Error opening/creating file. ")
        print("[-] ")

    #search against the temp list, output is json. Microsoft has several API's for search, this uses the basic web search.
    try:
        with open("/tmp/bing_hosts.txt", "r") as w:
            for line in w:
                search = "ip:" + line
                host = "api.cognitive.microsoft.com"
                path = "/bing/v7.0/search"
                headers = {'Ocp-Apim-Subscription-Key': api_key}
                conn = http.client.HTTPSConnection(host)
                query = urllib.parse.quote(search)
                conn.request("GET", path + "?q=" + query, headers=headers)
                response = conn.getresponse()
                result = response.read().decode("utf8")
                with open(filename, "a+") as outfile:
                    print(json.dumps(json.loads(result), indent=4), file=outfile)

    except (OSError, IOError):
        print("[-] ")
        print("[-] Error ")
        print("[-] ")	


def cleanup():
    #making sure the IP temp file is removed after processing.
    try:
        if os.path.exists("/tmp/bing_hosts.txt"):
            os.system("rm -r /tmp/bing_hosts.txt")			

    except (OSError,IOError):
        print ("[-] ")
        print ("[-] Problem deleting temp file. Check file permissions. ")
        print ("[-] ")


def main(argv):
	
    global ip_range
    global filename
    global api_key

    #Your Microsoft Bing API key goes here.
    api_key = "<API_KEY_GOES_HERE>"

    try:
        opts, args = getopt.getopt(argv, "hr:f:",["ip_range=","filename="])

    except getopt.GetoptError:		
        print (errors)
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print (errors)
            sys.exit()
        elif opt in ("-r", "--ip_range"):
            ip_range = arg
        elif opt in ("-f", "--filename"):
            filename = arg
	
    try:
        if os.path.exists(filename):
            print ("[+] ")
            print ("[+] File: " + filename + " already exists! Please remove the old file or type in a new path/filename. ")
            print ("[+] ")
            sys.exit()
    except (OSError, IOError):
        print ("[-] ")
        print ("[-] Problem writing to ", filename)
        print ("[-] ")
	

if __name__ == "__main__":

    while True:
        try:
            main(sys.argv[1:])
            search(sys.argv[1:])
            cleanup()
            break

        except IOError:
            print (errors)
            break

        except KeyboardInterrupt:
            print ("")
            print ("[+] ")
            print ("[+] Ctrl ^C, Aborted by user. ")
            print ("[+] ")
            sys.exit(3)	
	
