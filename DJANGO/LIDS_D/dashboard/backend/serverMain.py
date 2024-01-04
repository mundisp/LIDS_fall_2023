#! /usr/bin/env python3
import socket
import os
import time
import threading
import json
import sys
from collections import defaultdict
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from .database import establishDBConnection, insertAlert, Alert
from .ingestConfig import get_LNIDS_config

insert_alert_lock = threading.Lock()

def handleConnection(socketConnection, ipAddress):
    global userDict
    if ipAddress not in userDict:
        userDict[ipAddress] = {'Alerts': [], 'PCAPS': []}
    print(f"Client {ipAddress} connected.")
    
    # Create a new database connection for this thread
    dbConnection = establishDBConnection('../../lids-d_alertDB.sqlite3')
    
    try:
        while True:
            receiveData(socketConnection, ipAddress, dbConnection)
    except socket.timeout:
        socketConnection.settimeout(None)
    finally:
        # Close the database connection when the thread is done
        dbConnection.close()

def receiveData(socketConnection, ipAddress, dbConnection):
    global userDict
    # get key
    while True:
        socketConnection.settimeout(1)
        try:
            # decrypt
            filenameLength = socketConnection.recv(2).decode() # length of filename
            # blank data was causing errors
            if filenameLength == '':
                continue
            filename = socketConnection.recv(int(filenameLength)).decode() # filename (ALERT, DONE, or PCAP [not needed])
            if filename == 'DONE':
                print(f"Client {ipAddress} disconnected.")
                socketConnection.close()
                return
            if filename == 'ALERT':
                alertSize = int(socketConnection.recv(8).decode()) # alert size will never be more than 8 bytes
                alert = socketConnection.recv(alertSize).decode() # get alert data of size alertSize
                alert = json.loads(alert)
                alert = Alert.fromSerializable(alert)
                with insert_alert_lock:
                    insertAlert(dbConnection, alert)
                userDict[ipAddress]['Alerts'].append(alert.alertID)
                print(f"Alert {alert.alertID} received from {ipAddress}")
            else:
                filename = ipAddress + '_' + filename
                pcapSize = int(socketConnection.recv(8).decode())
                pcapBytes = socketConnection.recv(pcapSize)
                savePCAP(filename,pcapBytes)
                userDict[ipAddress]['PCAPS'].append(filename)
                print(f"PCAP {filename} received from {ipAddress}")

        except socket.timeout:
            socketConnection.settimeout(None)
            return tuple

def savePCAP(filename,pcapBytes):
    folder = 'LIDSD_server/pcaps/'
    file = open(filename,'wb')
    file.write(pcapBytes)
    file.close()

def serverMain(configPath):
    global userDict
    userDict = defaultdict(lambda: {'Alerts': [], 'PCAPS': []})
    dbConnection = establishDBConnection('../../lids-d_alertDB.sqlite3')
    print("Local database connection established.")
    serverInfo, config = get_LNIDS_config(configPath)
    host = serverInfo['ip']
    port = serverInfo['port']
    
    # if useConfig:
    #     serverInfo, config = get_LNIDS_config(configPath)
    #     host = serverInfo['ip']
    #     port = serverInfo['port']
    # else: # use default values
    #     host = 'localhost'
    #     port = 8080
    print("Server Starting...")
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((host, port))
    serverSocket.listen(10)
    print(f"\tHost: {host}\n\tPort: {port}")
    print("Server is listening...")
    start_time = time.time()
    while time.time() - start_time < 60:# run for 60 seconds
        socketConnection, [ipAddress,port] = serverSocket.accept()
        thread = threading.Thread(target=handleConnection, args=(socketConnection, ipAddress))
        thread.start()
    serverSocket.close()
    print("Server Stopped.")
    print("Data recieved:")
    for user in userDict:
        print(f"\tUser: {user}")
        print(f"\t\tAlerts: {userDict[user]['Alerts']}")
        print(f"\t\tPCAPS: {userDict[user]['PCAPS']}")

if __name__ == "__main__":
    useConfig = False
    if len(sys.argv) > 1:
        useConfig = sys.argv[1].upper() == 'TRUE'
    serverMain(useConfig)