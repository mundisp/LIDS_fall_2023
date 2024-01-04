#!/usr/bin/env python3

import pyshark
import sys

'''
This File contains functions to detect port scans in a pcap file using pyshark
'''

def isPortScan(fname,config={'portScanThreshold':5}):
    '''
    Determines if a pcap file contains a port scan
    params:
        fname: the path to the pcap file
        config: a dictionary of configuration parameters
    returns:
        messages: a list of messages describing the alerts
    '''
    messages = []
    messages+=isPortScanUDP(fname,config)
    messages+=isPortScanTCPSyn(fname,config)
    messages+=isPortScanTCPSynAck(fname,config)
    return messages

def isPortScanTCPSyn(fname,config={'portScanThreshold':5}):
    '''
    Determines if a pcap file contains a TCP SYN port scan (SYN flag set, ACK flag not set, time delta < 1/1500)
    params:
        fname: the path to the pcap file
        config: a dictionary of configuration parameters
    returns:
        alerts: an array of strings explaining each port scan
    '''
    with pyshark.FileCapture(fname, display_filter='tcp.flags.syn == 1 && tcp.flags.ack == 0 && frame.time_delta < 0.0066') as cap:
        portsPerIP_pair = {}
        result={}
        for packet in cap:
            try:
                key = str(packet.ip.src)+"*"+str(packet.ip.dst)
                if key not in portsPerIP_pair:
                    portsPerIP_pair[key] = []
                portsPerIP_pair[key].append(packet.tcp.dstport)
            except AttributeError:
                print('error at tcp syn')
                pass
        alerts = strPortScanDict(portsPerIP_pair,"TCP SYN")
    return alerts

def isPortScanTCPSynAck(fname,config={'portScanThreshold':5}):
    '''
    Determines if a pcap file contains a TCP SYN-ACK port scan (SYN flag set, ACK flag set, time delta < 1/1500)
    params:
        fname: the path to the pcap file
        config: a dictionary of configuration parameters
    returns:
        alerts: an array of strings explaining each port scan
    '''
    with pyshark.FileCapture(fname, display_filter='tcp.flags.syn == 1 && tcp.flags.ack == 1 && frame.time_delta < 0.0066') as cap:
        portsPerIP_pair = {}
        for packet in cap:
            try:
                key = str(packet.ip.src)+"*"+str(packet.ip.dst)
                if key not in portsPerIP_pair:
                    portsPerIP_pair[key] = []
                portsPerIP_pair[key].append(packet.tcp.dstport)
            except AttributeError:
                print('error at tcp syn-ack')
                pass
        alerts = strPortScanDict(portsPerIP_pair,"TCP SYN-ACK")
    return alerts

def isPortScanUDP(fname,config={'portScanThreshold':5}):
    '''
    Determines if a pcap file contains a UDP port scan (time delta < 1/1500)
    params:
        fname: the path to the pcap file
        config: a dictionary of configuration parameters
    returns:
        alerts: an array of strings explaining each port scan
    '''
    with pyshark.FileCapture(fname, display_filter='udp && frame.time_delta < 0.0066') as cap:
        portsPerIP_pair = {}
        result=False
        for packet in cap:
            try:
                key = str(packet.ip.src)+"*"+str(packet.ip.dst)
                if key not in portsPerIP_pair:
                    portsPerIP_pair[key] = []
                portsPerIP_pair[key].append(packet.udp.dstport)
            except AttributeError:
                print('error at tcp udp')
                pass
        alerts = strPortScanDict(portsPerIP_pair,"UDP")
    return alerts

def strPortScanDict(dict,protocol):
    '''
    splits a dictionary of the form {ip_src*ip_dst: [port1,port2,...]} into a list of strings of the form "<protocol> Portscan detected from <ip_src> to <ip_dst> on <n> ports"
    params:
        dict: the dictionary to split
        protocol: the protocol to use in the string
    returns:
        alerts: a list of strings describing the port scans
    '''
    protocol = protocol.upper()
    alerts = []
    for key,value in dict.items():
        src,dest = key.split("*")
        alerts.append(f"{protocol} Portscan detected from {src} to {dest} on {len(value)} ports")
    return alerts

if __name__ == '__main__':
    if len (sys.argv) < 2:
        # fname='./testPCAPs/3-ericka.pcapng'
        fname='./testPCAPs/5-evil.pcapng'
        # fname='./testPCAPs/udpPortScanSuccess.pcapng'
        # fname='./testPCAPs/synPortScanSuccess.pcapng'
    else:
        fname = sys.argv[1]
    print(f"Analyzing {fname} for nmap scans")
    messages = isPortScan(fname)
    print(len(messages),"port scans detected")