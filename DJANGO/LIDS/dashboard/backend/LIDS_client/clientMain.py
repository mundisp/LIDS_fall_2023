#!/usr/bin/env python3
import os
import socket
import time
import sys
import random
import json
from .encrypt import Encrypt
from .frame import Frame

# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from ingestConfig import get_LNIDS_config

alert_buf = [] # not using this right now. Might be useful if we have to store alerts before sending them
# The following 2 lines are for artificially generating user IDs. Later we'll get them from the config file
alert_users = ['Cris','Lianna','Edgar','Maria','Aldo','Edmundo','Daniel','Martin']
user = random.choice(alert_users)

# send alert to server
def sendAlert(socketConnection, alert):
    # 2 bytes for filename "ALERT"
    # 8 bytes for alert size ""
    # alert
    name = "ALERT"
    nameLength = len(name)
    done = "DONE"
    doneLength = len(done)
    alertString = alert.toJSON()
    alertLength = len(alertString)
    array = bytearray()
    array += f"{nameLength:02d}".encode() # name  length
    array += f"{name}".encode() # name
    array += f"{alertLength:08d}".encode() # alert length
    array += f"{alertString}".encode() # actual alert
    doneSent = f"{doneLength:02d}".encode()
    socketConnection.sendall(bytes(array))

#
# def sendPCAP(socketConnection, pcapFilePath):
#     # 2 bytes for filename
#     # 8 bytes for file size
#     # rest is file
#     file = open(pcapFilePath, 'rb')
#     fileName = os.path.basename(pcapFilePath)
#     array = bytearray()
#     array += f"{len(fileName):02d}".encode()
#     array += f"{fileName}".encode()
#     array += f"{os.path.getsize(pcapFilePath):08d}".encode()
#     array += file.read()
#     socketConnection.sendall(bytes(array), encoding='utf-8')

def connectToServer(serverInfo):
    host = serverInfo['ip']
    port = serverInfo['port']
    connected = False
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        clientSocket.connect((host, port))
        connected = True
        print(f"Connected to server {host} : {port}")
            # 1. send the key
    except:
        print(f"Could not connect to server {host} : {port}.")
    if connected:
        return clientSocket
    else:
        return None
    
#
# def generateTestAlert():
#     global alert_buf
#     global user
#     alert_id = random.randint(0,20000)
#     alert = generateDB.alertTupleToDict(generateDB.generateAlert(alert_id)) #saving the data as a tuple makes it easier for converting it to JSON
#     alert['user_id'] = user # adding the user_id field that the LIDS-D Alerts database will need
#     alert_buf.append(alert) # add to buffer, in the event we store them in a list before sending them. Not currently doing that tho
#     return alert
#
# def insert_LIDSD_Records(num=1000):
#     sql_command = sqlCommand = "INSERT OR IGNORE INTO alerts (alert_id, severity_level, time, ip_src, port_src, ip_dst, port_dst, length, protocol, info, descripton, filename, user_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
#     connection = generateDB.establishConnection('../../lids-d_alertDB.sqlite3')
#     cursor = connection.cursor()
#     for i in range(num):
#         vals = generateTestAlert()
#         val_tuple = (vals['alert_id'],vals['severity_level'],vals['time'],vals['ip_src'],vals['port_src'],vals['ip_dst'],vals['port_dst'],vals['length'], vals['protocol'],vals['info'],vals['description'],vals['filename'],vals['user_id'])
#         cursor.execute(sqlCommand, val_tuple)
#     connection.commit()
#     cursor.close()
#
# def handleConnection(conn):
#     current_directory = os.getcwd()
#     global user
#     conn.send(bytes(user, encoding='utf-8'))
#     while True:
#         send_alert = input(f"Enter 's' to send a random alert or 'e' to exit:\n>> ")
#         if send_alert == 's':
#             conn.send(b"OK")
#             time.sleep(0.5)
#             sendAlert(conn, generateTestAlert())
#             print(f"Alert has been sent")
#         elif send_alert == 'e':
#             conn.send(b'DONE')
#             print("Session ending...\n Goodbye!")
#             break
#         else:
#             print(f"invalid entry. Try again")

def clientMain(serverInfo):
    print("Starting client...")
    clientSocket = connectToServer(serverInfo)
    clientSocket.close()

if __name__ == "__main__":
    serverInfo, _ = get_LNIDS_config()
    clientMain(serverInfo)
