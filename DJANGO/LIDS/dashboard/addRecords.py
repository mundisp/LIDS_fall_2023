
import sqlite3
from django.db import models
#from models import Employee
from .models import Alert
from random import randint
from django.core.serializers import serialize
import random
from datetime import datetime

def insertRecords(num):
   
    reasonList = ['Port Scan', 'Failed Login', 'Unknown IP']
    portsList = ['80', '443' '1244', '22', '3211', '22444', '932']
    srcIPList = ['173.123.104.77', '33.149.184.47', '252.155.228.241', '60.125.174.149','41.248.208.21', '192.119.65.165']
    dstIPList = ['192.168.110.32', '192.168.110.34', '192.168.110.27']
    severityList = ['1','2','3','4']
    protocolList = ['TCP', 'FTP', 'UDP', 'RDP']
    infoList = ['HTTP/1.1 200 OK', '[TCP ZeroWindowProbe] 80 → 49201 [ACK] Seq=147105 Ack=524 Win=64240 Len=1 [TCP segment of a reassembled PDU]', '55527 → 5357 [SYN] Seq=0 Win=1024 Len=0 MSS=1460','DHCP ACK - Transaction ID 0x84ab3e19']
    filenameList = ['emptyDummy1.pcap','emptyDummy2.pcap','emptyDummy3.pcap']

    #make records with randomized data from the lists above for specified # records
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
        emp = Alert(Empid=randint(200,500), name='test', address='allsafe ave', salary=4321, Department='tech')  # create new model instance
        emp.save()
        pak=Alert(time=time,pLength=pLength,dstIP=dstIP,srcIP=srcIP,dstPort=dstPort,srcPort=srcPort,
                  protocol=protocol,severity=severity,reason=reason,info=info, filename=filename,)
        pak.save


if __name__ == '__main__':
    
    insertRecords( 100)
    #deleteRecords(connection)
    #printRecords(connection)





