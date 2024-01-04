#!/usr/bin/env python3

import pyshark
import time
import os
import multiprocessing
from database import establishDBConnection
from ingestConfig import get_LNIDS_config, get_LIDS_config, makeNodeMap, updateStatusNodeMap
from detectAlerts import analyzePacket, analyzePCAP

def capturePackets(packet_queue, config, output_folder, pcap_queue, capture_maxduration=None):
    start_time = time.time()
    pcapCount = 0

    while True:
        pcapFilename = f"SniffedPackets{pcapCount}.pcap"
        cwd = os.getcwd()
        file_path = cwd + '/' + output_folder + '/' + pcapFilename
        capture = pyshark.LiveCapture(output_file=file_path)
        capture.interfaces = config['interfaces']

        for packet in capture.sniff_continuously():
            packet_queue.put((packet, pcapFilename))

            if capture_maxduration and time.time() - start_time > capture_maxduration:
                packet_queue.put(None)  
                return  

            if time.time() - start_time > 10:  
                pcapCount += 1
                pcap_queue.put(file_path)
                start_time = time.time()  
                break

def packet_Analyzer(packet_queue, config, dbConnection, alertID,server_info):
    while True:
        packet, pcapFilename  = packet_queue.get()
        if packet is None:
            if dbConnection:
                dbConnection.close()
            return
        
        update = analyzePacket(dbConnection, packet, alertID.value, config, pcapFilename,server_info)
        if update:
            alertID = updateAlertID(alertID)

def pcap_Analyzer(pcap_queue, config, dbConnection,alertID,server_info):
    while True:
        pcapPath = pcap_queue.get()
        temp = None
        if temp != pcapPath:
            capture = pyshark.FileCapture(pcapPath)
            last_packet = None
            for packet in capture:
                last_packet = packet
            capture.close()

            update = analyzePCAP(pcapPath, config,alertID.value,dbConnection,last_packet,server_info)
            temp = pcapPath
            if update:
                alertID = updateAlertID(alertID)

def updateAlertID(alertID):
    alertID.value += 1
    return alertID

def createOutputFolder(output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

def main(ids,config_path):
    try:
        pcap_queue = multiprocessing.Queue()
        packet_queue = multiprocessing.Queue()
        alertID = multiprocessing.Value('i', 0)
        dbConnection = establishDBConnection('/BACKEND/LIDS_client/alerts.sqlite3')
        output_folder = 'BACKEND/trafficCaptures'

        createOutputFolder(output_folder)
        # makeNodeMap(config_path)

        if ids == 'LNIDS':
            server_info, config = get_LNIDS_config(config_path)
        elif ids == 'LIDS':
            server_info, config = get_LIDS_config(config_path)
            # updateStatusNodeMap(config, 'connected')


        capture_process = multiprocessing.Process(target=capturePackets, args=(packet_queue, config, output_folder, pcap_queue))
        splitBufferProcess = multiprocessing.Process(target=packet_Analyzer, args=(packet_queue, config,dbConnection,alertID,server_info))
        pcap_analyze_process = multiprocessing.Process(target=pcap_Analyzer, args=(pcap_queue, config, dbConnection,alertID,server_info))

        splitBufferProcess.start()
        pcap_analyze_process.start()
        capture_process.start()

    except KeyboardInterrupt:
        print("Terminating...")
        updateStatusNodeMap(config, 'terminated')

        if dbConnection:
            dbConnection.close()

        os._exit(0)

if __name__ == '__main__':
    if len(os.sys.argv) > 2:
        arg1 = os.sys.argv[1]  
        arg2 = os.sys.argv[2]  
        main(arg1,arg2)
    else:
        print("Insufficient arguments provided.")
        print("Usage: python script.py <arg1> <arg2>")
        print("Usage: <arg1> LIDS or LNIDS")
        print("Usage: <arg2> config file")
        os.sys.exit(1)  # Exit the script with an error code