#!/usr/bin/python3
#xx0hcd
#take a CIDR range and run reverse DNS lookups.
import argparse
import ipaddress
import subprocess
import sys
import dns.resolver,dns.reversename

def ip_gen(ip_arg):

	str1 = ip_arg.c
	ips2 = ipaddress.ip_network(str1)

	with open("/tmp/jU8e63nhGI.txt", "a") as f:
		for a in ips2:
			f.write(str(a) + "\n" )

def dns_rev(file_arg):
	with open("/tmp/jU8e63nhGI.txt", "r") as f:

		for line in f:

			words = line.split(" ")
			for bit in '01':
				ip = []
				for word in words:
					byte=word.replace('*', bit).strip()
					ip.append(str(byte))
			jnd = '.'.join(ip)
			fnd = file_arg.o

			with open(fnd, "a") as i:
		
				try:
					revdns = dns.reversename.from_address(jnd)
					soc = str(dns.resolver.query(revdns, "PTR")[0])
					i.write(str(soc) + "\n")
					
				except:
					continue


def main():
	global ip_arg
	global file_arg
	parser = argparse.ArgumentParser(description="Generate a list of IP's then run reverse DNS lookup on them, ./rev_dns.py -c <CIDR_range> -o <output_file>.")
	parser.add_argument('-c', type=str, help="Enter CIDR range i.e. 192.168.1.0/24" )
	parser.add_argument('-o', type=str, help="Enter name and location for output file")

	ip_arg = parser.parse_args()
	file_arg = parser.parse_args()
		

if __name__ == "__main__":
	while True:
		global ip_arg
		global file_arg
		
		try:
			main()
			ip_gen(ip_arg)
			print("[+] The reverse DNS list is being generated.")
			print("[+] This part can take a while... ")
			dns_rev(file_arg)
			break
			
		except IOError:
			print(errors)
			break

		except KeyboardInterrupt:
			print ("[+]")
			print ("[+] Ctrl ^C, Aborted by user. ")
			print ("[+]")
			sys.exit(3)
	subprocess.call(['rm', '-r', '/tmp/jU8e63nhGI.txt'])
	print("[+] Reverse DNS list is complete")
	print("[+] Finshed.")
