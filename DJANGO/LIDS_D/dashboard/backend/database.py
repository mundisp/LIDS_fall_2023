import sqlite3
import random
import os
import json
from datetime import datetime

'''
This code is for generating 'alerts.sqlite3' sqlite3 database with dummy alert data.
The alert data is randomized in the insertRecords() method. This code DOES NOT make real alerts 
based off of network traffic.
There are three methods to run: 
insertRecords(numRecords): Generates the specified # of records in the alert DB
printRecords(): Gets all records from the DB and prints them out
deleteRecords(): Clears all data from the alerts table.

You must comment out the the methods in the main method that you don't want to use.

Basics of using sqlite3
1. import sqlite3
2. use connection = sqlite3.connect('alert.db') to open up/create a .db file ('alert.db can be replaced with any .db file name)
3. use cursor = connection.cursor() to be able to interact w/ the DB
4. use cursor.execute(<sql-command>) to run the command on the DB
5. use connection.commit() to send the command to the DB
6. use cursor.close() to stop interacting w/ the DB
** There are many other cursor commands that you can see here: https://www.tutorialspoint.com/python_data_access/python_sqlite_cursor_object.htm
'''

## Database Schema
'''alerts table:
    alert_id: number (primary key)
    severity_level: text
    time: timestamp
    ip_src: text
    port_src: integer
    ip_dst: text
    port_dst: integer
    length: integer
    protocol: text
    reason: text
    filename: text
'''

class Alert:
    def __init__(self, alertID, packet, reason, pcapFilename, severity):
        self.alertID = alertID
        self.packet = packet
        self.reason = reason
        self.pcapFilename = pcapFilename
        self.severity = severity

        self.time = None
        self.srcIP = None
        self.srcPort = None
        self.dstIP = None
        self.dstPort = None
        self.length = None
        self.protocol = None

        if hasattr(packet, 'sniff_time'):
            self.time = packet.sniff_time

        if hasattr(packet, 'ip') and hasattr(packet.ip, 'src'):
            self.srcIP = packet.ip.src

        if hasattr(packet, 'tcp') and hasattr(packet.tcp, 'srcport'):
            self.srcPort = packet.tcp.srcport

        if hasattr(packet, 'ip') and hasattr(packet.ip, 'dst'):
            self.dstIP = packet.ip.dst

        if hasattr(packet, 'tcp') and hasattr(packet.tcp, 'dstport'):
            self.dstPort = packet.tcp.dstport

        if hasattr(packet, 'length'):
            self.length = packet.length

        if hasattr(packet, 'transport_layer'):
            self.protocol = packet.transport_layer

    @classmethod
    def fromSerializable(cls, serializable_data):
        alert = cls(
            alertID=serializable_data["alertID"],
            packet=None,  # You may set this to None or omit it as needed
            reason=serializable_data["reason"],
            pcapFilename=serializable_data["pcapFilename"],
            severity=serializable_data["severity"]
        )

        alert.time = datetime.strptime(serializable_data["time"], '%Y-%m-%d %H:%M:%S') if serializable_data["time"] else None
        alert.srcIP = serializable_data["srcIP"]
        alert.srcPort = serializable_data["srcPort"]
        alert.dstIP = serializable_data["dstIP"]
        alert.dstPort = serializable_data["dstPort"]
        alert.length = serializable_data["length"]
        alert.protocol = serializable_data["protocol"]

        return alert

    def toSQLValues(self):
        vals = (self.alertID, self.severity, self.time, self.srcIP, self.srcPort, self.dstIP, self.dstPort, self.length, self.protocol, self.reason, self.pcapFilename)
        return vals

    def toSerializable(self):
        # Create a dictionary with only the necessary attributes for serialization
        serializable_data = {
            "alertID": self.alertID,
            "reason": self.reason,
            "pcapFilename": self.pcapFilename,
            "severity": self.severity,
            "time": self.time.strftime('%Y-%m-%d %H:%M:%S') if self.time else None,
            "srcIP": self.srcIP,
            "srcPort": self.srcPort,
            "dstIP": self.dstIP,
            "dstPort": self.dstPort,
            "length": self.length,
            "protocol": self.protocol
        }
        return serializable_data

    def toJSON(self):
        return json.dumps(self.toSerializable(), sort_keys=True, indent=4)


def establishDBConnection(filepath='LIDS_client/alerts.sqlite3'):
    curDirectory = os.path.dirname(os.path.abspath(__file__))
    databasePath = os.path.join(curDirectory, filepath)
    connection = sqlite3.connect(databasePath)  
    # open the alerts database or create it if it doesn't exist
    cur = connection.cursor()
    table_query = '''
        CREATE TABLE IF NOT EXISTS alerts (
            alert_id INTEGER PRIMARY KEY,
            severity_level TEXT,
            time TIMESTAMP,
            ip_src TEXT,
            port_src INTEGER,
            ip_dst TEXT,
            port_dst INTEGER,
            length INTEGER,
            protocol TEXT,
            reason TEXT,
            filename TEXT
        )
    '''
    cur.execute(table_query)
    connection.commit()
    return connection

def insertDummyRecords(connection, num):
    cursor = connection.cursor()
    # Will only insert new values into the table on the first run of this script unless you run deleteRecords first
    sqlCommand = "INSERT OR IGNORE INTO alerts (alert_id, severity_level, time, ip_src, port_src, ip_dst, port_dst, length, protocol, reason, filename) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

    reasonList = ['Port Scan', 'Failed Login', 'Unknown IP']
    portsList = ['80', '443', '1244', '22', '3211', '22444', '932']
    srcIPList = ['173.123.104.77', '33.149.184.47', '252.155.228.241', '60.125.174.149', '41.248.208.21', '192.119.65.165']
    dstIPList = ['192.168.110.32', '192.168.110.34', '192.168.110.27']
    severityList = ['1', '2', '3']
    protocolList = ['TCP', 'FTP', 'UDP', 'RDP']
    infoList = ['HTTP/1.1 200 OK', '[TCP ZeroWindowProbe] 80 → 49201 [ACK] Seq=147105 Ack=524 Win=64240 Len=1 [TCP segment of a reassembled PDU]', '55527 → 5357 [SYN] Seq=0 Win=1024 Len=0 MSS=1460', 'DHCP ACK - Transaction ID 0x84ab3e19']
    filenameList = ['emptyDummy1.pcap', 'emptyDummy2.pcap', 'emptyDummy3.pcap']

    # Make records with randomized data from the lists above for the specified number of records
    for i in range(num):
        time = datetime.now()
        pLength = random.randrange(1001)
        dstIP = random.choice(dstIPList)
        srcIP = random.choice(srcIPList)
        dstPort = random.choice(portsList)
        srcPort = random.choice(portsList)
        protocol = random.choice(protocolList)
        severity = random.choice(severityList)
        reason = random.choice(reasonList)
        info = random.choice(infoList)
        filename = random.choice(filenameList)
        vals = (str(i), severity, time, srcIP, srcPort, dstIP, dstPort, pLength, protocol, reason, filename)
        cursor.execute(sqlCommand, vals)
    connection.commit()
    cursor.close()

def insertAlert(connection, alert):
    cursor = connection.cursor()
    sqlCommand = "INSERT OR IGNORE INTO alerts (alert_id, severity_level, time, ip_src, port_src, ip_dst, port_dst, length, protocol, reason, filename)"
    sqlCommand += "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    values = alert.toSQLValues()
    cursor.execute(sqlCommand, values)
    connection.commit()
    cursor.close()

def printRecords(connection):
    cursor = connection.cursor()
    sqlite_select_query = """SELECT * from alerts"""
    cursor.execute(sqlite_select_query)
    records = cursor.fetchall()  # get all values from the query in a list of tuples
    print("Total rows are:  ", len(records))
    print("Printing each row")
    for row in records:
        print("alertID: ", row[0])
        print("Severity: ", row[1])
        print("Time: ", row[2])
        print("srcIP: ", row[3])
        print("srcPort: ", row[4])
        print("dstIP: ", row[5])
        print("dstPort: ", row[6])
        print("length: ", row[7])
        print("Protocol: ", row[8])
        print("reason: ", row[9])
        print("pcap file: ", row[10])

        print("\n****************************************************\n")

    cursor.close()

def deleteRecords(connection):
    cursor = connection.cursor()
    command = "DELETE FROM alerts"
    cursor.execute(command)
    connection.commit()
    cursor.close()

if __name__ == '__main__':
    connection = establishDBConnection()
    insertDummyRecords(connection, 1000)





