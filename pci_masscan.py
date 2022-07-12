#script using masscan for 'PCI segment scanning'.
#main requirement -> all TCP and UDP ports scanned and each scanned range to have its own report. Tested on Windows 10 and Python 3.9.4.
#uses python subprocess instead of python-masscan.
#xx0hcd

import time
import re
import sys
import subprocess
import os, glob
from pathlib import Path

#requires python tqdm for progress tracking -> pip install tqdm - windows might need 'python -m pip install tqdm'
from tqdm import tqdm

#masscan arguments
mas_ports = "-p 1-65535,U:1-65535"
#mas_ports = "-p 22,80,443"

#set rate limit here
mas_rate = "--rate=5000"

#set number of NIC interface to use here, found via CMD "masscan.exe --iflist"
mas_nic = "3"

#define path with line separated hosts, must be named 'targets.txt'
host_path = "C:\\Users\\xx0hcd\\Desktop\\masscan\\targets.txt"

#define path to write the output file to.
out_path = "C:\\Users\\xx0hcd\\Desktop\\masscan\\reports\\"

def scanrun():
    try:
        #open host file, will loop one line at a time. if the line is a large CIDR range it might take awhile.
        with open(host_path, 'r') as targets:
    
            #using tqdm to track scan progress in the console.
            for host in tqdm(targets.readlines()):
        
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
                #add .txt for file extension
                output += ".txt"
                
                try:
                    
                    #extra timeout/sleep to get around buffer/timeout issues. Might have to adjust these..
                    print("\n [+] Pausing 10 seconds before start...")
                    time.sleep(10)

                    #open the output file/location and write subprocess stdout to it.
                    with open(output, 'a') as f:
                    
                        cmd = ["timeout", "/t", "10", ">null", "&&", "masscan.exe", host.rstrip('\n'), mas_ports, mas_rate, "-e", mas_nic, "&&", "timeout", "/t", "10", ">null"]
                        startScan = subprocess.run(cmd, shell=True, stdout=f)
                        print("[+] Writing to report, ready in @10 seconds. ")
                        time.sleep(10)
                    
                except Exception as e:
                    print("[-] Error in scan loop -> ",e)
                    continue
           
    except Exception as e:
        print("[-] Error: ",e)

def cleanup():
    time.sleep(5)
    #files remain empty if no ports were found. find files of size zero and enter some text that nothing was found.
    pathlist = Path(out_path).glob('*.txt')
    for path in pathlist:
        file1 = str(path)
        if os.path.getsize(file1) == 0:
            with open(file1, "a") as f:
                print("No TCP or UDP ports found during scan. ",file=f)
        else:
            continue


def main():
    scanrun()
    print("[+] Sleep 10 before cleanup...")
    time.sleep(10)
    cleanup()
    
if __name__ == "__main__":
    try:       
        main()       
        print("[+] Scanning is finished. ")
    except IOError as e:
        print(e)
    #this error will display if the scan is canceled by Ctrl^C, etc.
    except KeyboardInterrupt:
        print("[+] Cancelled by user.")
        sys.exit(3)
