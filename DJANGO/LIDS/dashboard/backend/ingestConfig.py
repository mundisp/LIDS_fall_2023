#!/usr/bin/env python3
import re
import os
import sys
from pathlib import Path
import socket
import psutil 

def get_LNIDS_config(filepath):
    '''
    Reads the config file and returns a dictionary of its contents
    params:
        filepath: the path to the config file
    returns:
        config_info: a dictionary of the form {ip: {name, mac, ports, whitelist}}
    '''
    target_dir = Path(filepath)
    if not target_dir.exists():
        print(f"************\nCONFIG FILE AT: {filepath} DOES NOT EXIST.\n Using sample configuration file"+
              ", alert detection/server connection may be inaccurate.\n************")
        parentDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        filepath = os.path.join(parentDir, "config.xml")
    else:
        parentDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        filepath = os.path.join(parentDir, filepath)

    fileData = None
    config_info={}
    serverInfo = {}
    try:
        with open(filepath, 'r') as f:
            fileData = f.read()
    except:
        print("ERROR OPENING THE FILE. TRY RUNNING PROGRAM AGAIN.\nENDING PROGRAM...")
        raise SystemExit(1)

    #Get server info
    serverSection = fileData.split('</server>')[0]

    serverIP_regex = r"<ip>(.*?)</ip>"
    serverIP = re.search(serverIP_regex, serverSection)


    serverPort_regex = r"<port>(.*?)</port>"
    serverPort = re.search(serverPort_regex, serverSection)

    serverInfo['ip'] = serverIP.group(1)
    serverInfo['port'] = int(serverPort.group(1))

    #Get interface info
    interfaceSection = fileData.split('</interfaces>')[0]
    interfaces_regex=r"<interfaces>(.*?)</interfaces>"
    interfaces=re.search(interfaces_regex,interfaceSection)
    if interfaces:
        interfaces=interfaces.group(1)
        interfaces=list(interfaces.split(','))
    else:
        # interfaces=['eth0']
        interfaces=['any']
    config_info['interfaces']=interfaces
    
    #Get port scan threshold
    portScanSection = fileData.split('</portScanThreshold>')[0]
    ps_threshold_regex=r"<portScanThreshold>(.*?)</portScanThreshold>"
    ps_threshold=re.search(ps_threshold_regex,portScanSection)
    if ps_threshold:
        ps_threshold=ps_threshold.group(1)
        ps_threshold=int(ps_threshold)
    else:
        ps_threshold=5
    config_info['portScanThreshold']=ps_threshold

    #Get whitelist info
    for line in fileData.split('<system>'):
        if line:
            name_regex=r"<name>(.*?)</name>"
            name=re.search(name_regex,line)
            if name:
                name=name.group(1)
            ip_regex = r"<ip>(.*?)</ip>"
            ip = re.search(ip_regex, line)
            if ip:
                ip = ip.group(1)
            mac_regex=r"<mac>(.*?)</mac>"
            mac=re.search(mac_regex,line)
            if mac:
                mac=mac.group(1)
            port_regex=r"<ports>(.*?)</ports>"
            ports=re.search(port_regex,line)
            if ports:
                ports=ports.group(1)
                ports=set(ports.split(','))
            whitelist_regex=r"<whitelist>(.*?)</whitelist>"
            whitelist=re.search(whitelist_regex,line)
            if whitelist:
                whitelist=whitelist.group(1)
                whitelist=set(whitelist.split(','))
            if name and ip and mac and ports and whitelist:  
                config_info[ip]={
                    'name':name,                    
                    'mac':mac,
                    'ports':ports,
                    'whitelist':whitelist,
                }
    return serverInfo, config_info

def get_device_ip():
    for interface, snics in psutil.net_if_addrs().items():
        for snic in snics:
            if snic.family == socket.AF_INET and not snic.address.startswith("127.") and (interface=='eth0' or interface=='enp0s3'):
                device_ip =  snic.address
    return device_ip

def get_LIDS_config(filename):
    '''
    Reads the config file and returns a dictionary of its contents for the current device
    params:
        filename: the path to the config file
    returns:
        config_info: a dictionary of the form {ip: {name, mac, ports, whitelist}}
    '''
    device_ip = get_device_ip()

    serverInfo, full_config = get_LNIDS_config(filename)
    if device_ip in full_config:
        lids_dict = {device_ip:full_config[device_ip]}
        lids_dict['portScanThreshold'] = full_config['portScanThreshold']
        lids_dict['interfaces'] = full_config['interfaces']
        return serverInfo, lids_dict
    else:
        print(f"Device IP {device_ip} not found in config file")

def makeNodeMap(config):
    '''
    Creates a nodeMap file with the status of each device
    params:
        config: a dictionary of the form {ip: {name, mac, ports, whitelist}}
        status: the status of the device
    '''
    config = config[1]
    print("Making nodeMap...")
    status = 'not Started'
    #make file if it doesn't exist
    cwd = os.getcwd()
    nodeMapFilePath = cwd + 'nodeMap.txt'
    if not os.path.exists(nodeMapFilePath):
        with open(nodeMapFilePath, 'w') as f:
            f.write("")
    #check if file is empty
    with open(nodeMapFilePath, 'r') as f:
        lines = f.readlines()
    # add all ips to file
    # if len(lines) == 0:
    #     with open(nodeMapFilePath, 'w') as f:
    #         for ip in config.keys():
    #             if ip == 'portScanThreshold' or ip == 'interfaces':
    #                 continue
    #             f.write(f"{ip}, {config[ip]['name']}, {status}\n")

def updateStatusNodeMap(config, status):
    '''
    Updates the status of the device in the nodeMap
    params:
        config: a dictionary of the form {ip: {name, mac, ports, whitelist}}
    '''
    if status not in ['connected', 'not Started', 'terminated']:
        print("Invalid status")
        return
    nodeMapFilePath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "nodeMap.txt")
    for interface, snics in psutil.net_if_addrs().items():
        for snic in snics:
            if snic.family == socket.AF_INET and not snic.address.startswith("127.") and (interface=='eth0' and interface=='enp0s3'):
                device_ip =  snic.address
    name = config[device_ip]['name']
    with open(nodeMapFilePath, 'r') as f:
        lines = f.readlines()
    with open(nodeMapFilePath, 'w') as f:
        for line in lines:
            if line.startswith(device_ip):
                f.write(f"{device_ip} {name} {status}\n")
            else:
                f.write(line)

def clearNodeMap():
    '''
    Clears the nodeMap file
    '''
    nodeMapFilePath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "nodeMap.txt")
    with open(nodeMapFilePath, 'w') as f:
        f.write("")

if __name__ == '__main__':
    print(gethostbyname(gethostname()))
