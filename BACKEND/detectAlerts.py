#!/usr/bin/env python3
'''
This program currently only detects alerts from a PCAP
'''
from portScan import isPortScan
from loginAttempt import isFailedLoginAttempt, analyze_failed_login_attempts
import sys
import ingestConfig
from database import insertAlert as insertAlertDB
from LIDS_client.clientMain import sendAlert as sendAlertServer
from database import Alert
import os
from LIDS_client.clientMain import connectToServer

def analyzePCAP(pcapPath, config,alertID,dbConnection, last_packet, server_info):
    '''
    Checks a pcap file for alerts
    params:
        filename: the path to the pcap file
        config: a dictionary of configuration parameters
    returns:
        messages: a list of messages describing the alerts
    '''
    messagesPS = isPortScan(pcapPath,config)
    messagesLA = analyze_failed_login_attempts(pcapPath)
    output = messagesLA+messagesPS
    pcapFilename = os.path.basename(pcapPath)
    if output:
        alert = Alert(alertID,last_packet,'Port Scan', pcapFilename, '3')
        insertAlertSendAlert(dbConnection,server_info,alert,alertID,messagesPS[-1],'3')
        return True
    return False
    

def analyzePacket(dbConnection, packet, alertID, config, pcapFilename, server_info):
    '''
    Determines if a packet is malicious
    params:
        packet: the packet to analyze
        config: a dictionary of configuration parameters
    returns:
        messages: a list of messages describing the alerts
        level: the level of the alert
    '''
    message=isFailedLoginAttempt(packet)
    Login_alert = len(message)>0
    IP_alert = None
    IP_alert = maliciousIP(packet,config)
    level=None
    if IP_alert:
        message+="Malicious IP"
    if IP_alert and Login_alert:
        level= "3" # HIGH
    elif not IP_alert and Login_alert:
        level= "2" # MEDIUM
    elif IP_alert and not Login_alert:
        level= "1" # LOW
    if IP_alert or Login_alert:
        print('alert gen')
        alert = Alert(alertID, packet, message, pcapFilename, level)
        insertAlertSendAlert(dbConnection,server_info,alert,alertID,message,level)
        return True
    return False

alerts_buffer = []
def insertAlertSendAlert(dbConnection,server_info,alert,alertID,message,level):
    global alerts_buffer  # Declare alerts_buffer as global
    serverConnection = connectToServer(server_info)

    if dbConnection:
        insertAlertDB(dbConnection, alert)

    if serverConnection is not None:
        # Send all buffered alerts first
        while alerts_buffer:
            buffered_alert = alerts_buffer.pop(0)
            print("Sending buffered alert")
            sendAlertServer(serverConnection, buffered_alert)

        # Send the current alert
        sendAlertServer(serverConnection, alert)
    else:
        # If no server connection, buffer the alert
        alerts_buffer.append(alert)

    print(f"Alert {alertID} detected: {message} level {level}")

def maliciousIP(packet, config):
    '''
    Determines if a packet is from a malicious IP
    params:
        packet: the packet to analyze
        config: a dictionary of configuration parameters
    returns:
        True if the packet is from a malicious IP, False otherwise
    '''
    try:
        dest = packet.ip.dst
        src = packet.ip.src
        return dest in config and src not in config[dest]['whitelist']
    except AttributeError:
        print("atrb error")
        return False

if __name__ == '__main__':
    if len (sys.argv) < 2:
        # fname='./testPCAPs/3-ericka.pcapng'
        fname='./testPCAPs/5-evil.pcapng'
        # fname='./testPCAPs/udpPortScanSuccess.pcapng'
        # fname='./testPCAPs/synPortScanSuccess.pcapng'
    else:
        fname = sys.argv[1]
    serverinfo,config = ingestConfig.get_LNIDS_config()
    analyzePCAP(fname,config)