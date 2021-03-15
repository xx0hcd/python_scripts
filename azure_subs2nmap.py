#!/usr/bin/python3
#using azure management api (not the SDK), calls to get public IP from available subscriptions.
#temp api key - auth = https://docs.microsoft.com/en-us/rest/api/virtualnetwork/publicipaddresses/listall - click 'Try It!', log in, grab the token.
#Modified from the other azure script I have, this one goes through the subscriptions you have access to and pulls out the public IP's in a format that works with nmap's -iL.
#xx0hcd

import requests
import pathlib
import json
import sys
import subprocess
from tqdm import tqdm

#paste api key here.
api_key = ''

headers = {'Authorization': 'Bearer {0}'.format(api_key)}

def temp_file():
#set up a file to temp store subscription names.
    try:
        #/tmp/temp.txt holds the subscription ID's to iterate through.
        x = pathlib.Path('/tmp/temp.txt')
        #/tmp/final_out.txt holds line separated IP's for the nmap list.
        y = pathlib.Path('/tmp/final_out.txt')
        if x.exists() == True:
            pathlib.Path.unlink(x)
        else:
            pathlib.Path(x).touch()
        if y.exists() == True:
            pathlib.Path.unlink(y)
        else:
            pathlib.Path(y).touch()
    except:
        pass

def get_sub_ids():
#get all subscription ID's we have access to.
    uri = 'https://management.azure.com/subscriptions?api-version=2019-11-01'

    try:
        api_call = requests.get(uri, headers=headers)
        out = api_call.text
        out2 = json.loads(out)
        if api_call.status_code == 200:
            print("[+] Starting, this could take a few.. ")
        elif 'ExpiredAuthenticationToken' in out2['error']['code']:
            print("Expired Authentication Token, time to get a new one.")
            exit()
        elif api_call.status_code == 401:
            print("Authentication Failed, check API Key.")
            exit()

        if api_call.status_code == 200:
            temp_file()
            i = 0
            while i < len(out2['value']):
                if 'subscriptionId' in out2['value'][0]:
                    print(out2['value'][i]['subscriptionId'], file=open('/tmp/temp.txt', 'a'))
                    i += 1
    except KeyError:
        pass

def uri_setup():
#loop subscription IDs for public IP/FQDN.
    with open('/tmp/temp.txt', 'r') as sub_ids:
        for ids in tqdm(sub_ids.readlines()):
            ids = ids.strip('\n')

            #not sure how often the api version changes, of course that means change it here too.
            uri = 'https://management.azure.com/subscriptions/' + ids + '/providers/Microsoft.Network/publicIPAddresses?api-version=2019-11-01'
            api_call = requests.get(uri, headers=headers)
            out1 = api_call.json()
            out2 = api_call.text
            out3 = json.loads(out2)
            try:
                i = 0
                while i < len(out1['value']):
                    if 'ipAddress' in out3['value'][0]['properties']:
                        print(out3["value"][i]["properties"]["ipAddress"], file=open('/tmp/final_out.txt', 'a'))
                    i += 1
                    
            except:
                pass
                

def main():
        get_sub_ids()
        uri_setup()

if __name__ == "__main__":
    try:       
        main()
        print("[+] Finished. Output at /tmp/final_out.txt. ")
    except IOError as e:
        print(e)

    except KeyboardInterrupt:
        print("[+] Aborted by user.")
        sys.exit(3)
