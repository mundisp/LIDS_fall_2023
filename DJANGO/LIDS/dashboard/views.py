import subprocess

from django.shortcuts import render, HttpResponse
from .models import Alert
from random import randint
from django.core.serializers import serialize
import random
from datetime import datetime
from pathlib import Path
import psutil
from django.core.files.storage import FileSystemStorage
from .backend.ingestConfig import get_device_ip


def getAlert():
    objects = Alert.objects.all()
    return objects

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

        pak=Alert(time=time,pLength=pLength,dstIp=dstIP,srcIP=srcIP,dstPort=dstPort,srcPort=srcPort,
                  protocol=protocol,severity=severity,reason=reason,info=info, filename=filename)
        pak.save()

# Create your views here.
def default(request):
    return render(request, 'default.html')

def PCAPs(request):
    return render(request, 'PCAPs.html')

def getSpace():
    disk_usage = psutil.disk_usage('/')
    free_space_gb = round(disk_usage.free / (2**30), 2)
    return free_space_gb

def Alerts(request):
    temp=getAlert()
    context={
        'alerts': temp,
        'free_space': getSpace(),
        'device_ip': get_device_ip(),
    }
    return render(request, 'Alerts.html',context)

def configUpload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        file_path = str(fs.path(filename))
        print(f"CONFIG FILE PATH: {file_path}")
        BASE_DIR = Path(__file__).resolve().parent
        lids_path = str(BASE_DIR) + '/backend/main.py'
        get_ip_path = str(BASE_DIR) + '/backend/injest_config.py'
        print(f" LIDS PATH: {lids_path}")
        command = ['python3', lids_path, 'LIDS', file_path]
        process = subprocess.Popen(command,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        context={
            'alerts': getAlert(),
            'free_space': getSpace(),
            'device_ip': get_device_ip(),
        }
        #return render(request, 'Alerts.html', context)
        return render(request, 'configComplete.html')
        

    return render(request, 'configUpload.html')

def welcomePage(request):
    return render(request, 'welcomePage.html')

def configComplete(request):
    return render(request, 'configComplete.html')

def TableBase(request):
    return render(request, 'TableBase.html')

def sort(request):
    insertEmployee()
    insertRecords(10)
    alerts=getAlert()
    data=getEmployee()
    context={
        'alerts': alerts
    }
    print(serialize("json", data))
    print("\n")
    print(serialize("json", alerts)) #using this to print out data to terminal for now.
    return render(request, 'sort.html', context)


