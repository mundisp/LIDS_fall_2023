import sqlite3
import random
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


def establishConnection(filePath='LIDS_client/alerts_test1.sqlite3'):
    connection = sqlite3.connect(filePath)  # open the alerts database or create it if it doesn't exist
    cur = connection.cursor()
    # create necessary tables - don't worry about the other two for now
    cur.execute('''CREATE TABLE IF NOT EXISTS alerts 
        (alert_id text PRIMARY KEY, severity_level text, time text, ip_src text, port_src text, ip_dst text, port_dst text, length text, protocol text, info text, descripton text, filename text, user_id text)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS MaliciousPCAPs
        (alert_id text PRIMARY KEY, reason text, filename text)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS MaliciousPacketsRaw
        (alert_id text PRIMARY KEY, packet text, reason text, filename text)''')
    return connection

def insertRecords(connection, num):
    cursor = connection.cursor()
    # will only insert new values into the table on the first run of this script unless you run deleteRecords first
    sqlCommand = "INSERT OR IGNORE INTO alerts (alert_id, severity_level, time, ip_src, port_src, ip_dst, port_dst, length, protocol, info, descripton, filename) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

    #make records with randomized data from the lists above for specified # records
    for i in range(num):
        vals = generateAlert(i)
        cursor.execute(sqlCommand, vals)
    connection.commit()
    cursor.close()
    return vals

def generateAlert(i):
    reasonList = ['Port Scan', 'Failed Login', 'Unknown IP']
    portsList = ['80', '443' '1244', '22', '3211', '22444', '932']
    srcIPList = ['173.123.104.77', '33.149.184.47', '252.155.228.241', '60.125.174.149', '41.248.208.21',
                 '192.119.65.165']
    dstIPList = ['192.168.110.32', '192.168.110.34', '192.168.110.27']
    severityList = ['1', '2', '3', '4']
    protocolList = ['TCP', 'FTP', 'UDP', 'RDP']
    infoList = ['HTTP/1.1 200 OK',
                '[TCP ZeroWindowProbe] 80 → 49201 [ACK] Seq=147105 Ack=524 Win=64240 Len=1 [TCP segment of a reassembled PDU]',
                '55527 → 5357 [SYN] Seq=0 Win=1024 Len=0 MSS=1460', 'DHCP ACK - Transaction ID 0x84ab3e19']
    filenameList = ['emptyDummy1.pcap', 'emptyDummy2.pcap', 'emptyDummy3.pcap']

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
    vals = (str(i), severity, str(time), srcIP, srcPort, dstIP, dstPort, pLength, protocol, info, reason, filename)
    return vals
def alertTupleToDict(alertTuple, alertFields= ['alert_id', 'severity_level', 'time', 'ip_src', 'port_src', 'ip_dst', 'port_dst', 'length', 'protocol', 'info', 'description', 'filename']):
    alertDict = {}
    for i in range(len(alertTuple)):
        alertDict[alertFields[i]] = alertTuple[i]
    return alertDict

def printRecords(connection):
    cursor = connection.cursor()
    sqlite_select_query = """SELECT * from alerts"""
    cursor.execute(sqlite_select_query)
    records = cursor.fetchall() #get all values from the query in list of tuples
    print("Total rows are:  ", len(records))
    print("Printing each row")
    for row in records:
        print("alertID: ", row[0])
        print("Severity: ", row[1])
        print("Time: ", row[2])
        print("srcIP: ", row[3])
        print("srcPort: ",row[4])
        print("dstIP: ", row[5])
        print("dstPort: ", row[6])
        print("length: ",row[7])
        print("Protocol: ",row[8])
        print("info: ", row[9])
        print("description: ",row[10])
        print("pcap file: ", row[11])

        print("\n****************************************************\n")

    cursor.close()

def print_LIDSD_Records(connection):
    cursor = connection.cursor()
    sqlite_select_query = """SELECT * from alerts"""
    cursor.execute(sqlite_select_query)
    records = cursor.fetchall() #get all values from the query in list of tuples
    print("Total rows are:  ", len(records))
    print("Printing each row")
    for row in records:
        print("alertID: ", row[0])
        print("Severity: ", row[1])
        print("Time: ", row[2])
        print("srcIP: ", row[3])
        print("srcPort: ",row[4])
        print("dstIP: ", row[5])
        print("dstPort: ", row[6])
        print("length: ",row[7])
        print("Protocol: ",row[8])
        print("info: ", row[9])
        print("description: ",row[10])
        print("pcap file: ", row[11])
        print("user ID: ", row[12])

        print("\n****************************************************\n")



def deleteRecords(connection):
    cursor = connection.cursor()
    command = "DELETE FROM alerts"
    cursor.execute(command)
    connection.commit()
    cursor.close()

if __name__ == '__main__':
    connection = establishConnection()
    #insertRecords(connection, 1000)
    #deleteRecords(connection)
    #printRecords(connection)





