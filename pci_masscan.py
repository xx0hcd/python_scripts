#script using python-masscan for 'PCI segment scanning'. - https://pypi.org/project/python-masscan/
#main requirement -> all TCP and UDP ports scanned and each scanned range to have its own report. 
#xx0hcd

#regex for formating file name output
import re

#pprint for nice output formatting
import pprint

#using sys for error handling
import sys

#requires python-masscan -> pip install python-masscan - windows might need 'python -m pip install python-masscan'
import masscan

#requires python tqdm for progress tracking -> pip install tqdm - windows might need 'python -m pip install tqdm'
from tqdm import tqdm


#set variable to use later for the scanning tasks.
mas = masscan.PortScanner()

#scan all TCP and UDP ports.
mas_ports = "1-65535,U:1-65535"

#in 'mas.scan()' below, arguments= will only take one variable so add all args to this 'mas_args' variable.
#interface for Windows OS show as numbers, use 'masscan --iflist' then change '-e' to whatever number interface you want. i.e. '-e 4'
mas_args = "--rate=500 -e 4"

#define path with line separated hosts, must be named 'targets.txt'
host_path = "C:\\Users\\xx0hcd\\Desktop\\masscan\\targets.txt"

#define path to write the output file to.
out_path = "C:\\Users\\xx0hcd\\Desktop\\masscan\\reports\\"

#use functions so things can be added easy later, argparse, etc.
def scanrun():
    try:
        #open host file, will loop one line at a time. if the line is a large CIDR range it might take awhile.
        with open(host_path, 'r') as targets:
    
            #using tqdm to track scan progress in the console.
            for host in tqdm(targets.readlines()):
        
                #starting the scan using defined arguements.
                try:
                
                    result = mas.scan(host, ports=mas_ports, arguments=mas_args)
                
                    #setting variable 'output' for output file naming.
                    output =  out_path + host
                
                    #remove any newlines
                    output = output.rstrip('\n')
                
                    #regex to capture any numbers after the slash
                    res = re.search(r"(\d+)$", output).group()
                    #get rid of the numbers
                    output = output.removesuffix(res)
                    #and also get rid of the slash
                    output = output.removesuffix("/")
            
                    #add .xml file extension
                    output += ".xml"
            
                    #Extra text to let us know the range is done, the file is written, and moving on
                    print("Printing file to: ",output)
				
				    #pprint to file. file name will be the range that was scanned, i.e. 'C:\Users\xx0hcd\Desktop\masscan\reports\192.168.0.0.xml'
                    with open(output, "a") as file:
                        pprint.pprint(mas.scan_result, file)
                
                #ran into this issue, so trying to work around it -> https://github.com/MyKings/python-masscan/issues/29
                #TL;DR -> if no ports are found python-masscan throws an exception, so lets ignore it and keep going               
                except Exception:
                    #lets keep our naming scheme and add some text that nothing was found...
                    output2 = out_path + host
                    output2 = output2.rstrip('\n')
                    res = re.search(r"(\d+)$", output2).group()
                    output2 = output2.removesuffix(res)
                    output2 = output2.removesuffix("/")
                    output2 += "_no_open_ports.txt"
                    with open(output2, "a") as file:
                        pprint.pprint("No open TCP or UDP ports were found in this scan", file)
                    continue
            
    except Exception:
        #if something goes wrong will print the exact error message, mostly useful during writing/debugging.
        print("Error: ",e)

       
def main():
    scanrun()
    
    
if __name__ == "__main__":
    try:       
        main()       
        print("[+] Scanning is finished. ")
    except IOError as e:
        print(e)
    #this error will display if the scan is canceled by Ctrl^C, etc.
    except KeyboardInterrupt:
        print("[+] Aborted by user.")
        sys.exit(3)
