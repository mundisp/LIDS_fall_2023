#! /usr/bin/env python3

import pyshark

### Analyze PCAP for failed login attempts ###
def analyze_ssh_failed_attempts(pcap_file):
    '''
    Detects failed SSH attempts (RST flag set on port 22)
    params:
        pcap_file: the path to the pcap file
    returns:
        result: a dictionary of the form {ip_src*ip_dst: count}
    '''
    with pyshark.FileCapture(pcap_file, display_filter='tcp.port == 22 && tcp.flags.reset == 1') as capture:
        pacs=0
        result = {}
        for packet in capture:
            key = str(packet.ip.src) + "*" + str(packet.ip.dst)
            if key not in result:
                result[key] = 1
            else:
                result[key] += 1
            pacs+=1
    return result

def analyze_ftp_failed_attempts(pcap_file):
    '''
    Detects failed FTP attempts (response code 530)
    params:
        pcap_file: the path to the pcap file
    returns:
        result: a dictionary of the form {ip_dst*ip_src: count}
    '''
    with pyshark.FileCapture(pcap_file, display_filter='ftp && ftp.response.code == 530') as capture:
        ftps=0
        result = {}
        for packet in capture:
            key = str(packet.ip.dst) + "*" + str(packet.ip.src)
            if key not in result:
                result[key] = 1
            else:
                result[key] += 1
            ftps+=1
    return result

def analyze_rdp_failed_attempts(pcap_file):
    '''
    Analyzes a pcap file for failed RDP attempts (RST flag set on port 3389)
    params:
        pcap_file: the path to the pcap file
    returns:
        result: a dictionary of the form {ip_dst*ip_src: count}       
    '''
    with pyshark.FileCapture(pcap_file, display_filter='tcp.port == 3389 && tcp.flags.reset == 1') as capture:
        rdps=0
        result = {}
        for packet in capture:
            key = str(packet.ip.dst) + "*" + str(packet.ip.src)+'*'+str(packet.tcp.srcport)
            if key not in result:
                result[key] = 1
            else:
                result[key] += 1
            rdps+=1
    return result

def analyze_failed_login_attempts(pcap_file):
    '''
    Counts the number of failed login attempts in a pcap file for each type
    params:
        pcap_file: the path to the pcap file
    returns:
        output: a dictionary of the form {protocol: {ip_src*ip_dst: count}}
    '''
    ssh_result = analyze_ssh_failed_attempts(pcap_file)
    ftp_result = analyze_ftp_failed_attempts(pcap_file)
    rdp_result = analyze_rdp_failed_attempts(pcap_file)
    output = dict()
    output['ssh'] = ssh_result
    output['ftp'] = ftp_result
    output['rdp'] = rdp_result
    return strAlerts(output)

def strAlerts(alerts):
    '''
    prints the alerts in a readable format
    params:
        alerts: a dictionary of the form {protocol: {ip_src*ip_dst: count}}
    returns:
        None
    '''
    alertMessages=[]
    for protocol, amount in alerts.items():
        alertMessages.append(f"{amount} total failed {protocol} login attempts")    
    return alertMessages   

## Analyze Packet for failed login attempts ##
def isFailedRDPAttempt(packet):
    '''
    Determines if a given packet is a failed RDP attempt (RST flag set on port 3389)
    params:
        packet: a pyshark packet
    returns:
        boolean: True if the packet is a failed RDP attempt, False otherwise
    '''
    try:
        return 'TCP' in packet and '3389' in packet['TCP'].dstport and packet['TCP'].flags_reset == 1
    except KeyError:
        return False

def isFailedFTPAttempt(packet):
    '''
    Determines if a given packet is a failed FTP attempt (response code 530)
    params:
        packet: a pyshark packet
    returns:
        boolean: True if the packet is a failed FTP attempt, False otherwise
    '''
    try:
        return 'FTP' in packet and packet['FTP'].response_code == '530'
    except KeyError:
        return False

def isTerminatedSSHConnection(packet):
    '''
    Determines if a given packet is a terminated SSH connection
    params:
        packet: a pyshark packet
    returns:
        boolean: True if the packet is a terminated SSH connection, False otherwise
    '''
    try:
        return 'TCP' in packet and '22' in packet['TCP'].dstport and packet['TCP'].flags_reset == 1
    except KeyError:
        return False

def isFailedLoginAttempt(packet):
    '''
    Detects if a packet is a failed password attempt.
    params:
        packet: a pyshark packet
    returns:
        messages: a list of strings indicating which protocols the packet is a failed password attempt for
    '''
    if isFailedFTPAttempt(packet):
        return "FTP"
    if isFailedRDPAttempt(packet,):
        return "RDP"
    if isTerminatedSSHConnection(packet):
        return "SSH"
    return ""

if __name__ == '__main__':
    pcap_file = './testPCAPs/3-ericka.pcapng'  # Replace with the path to your packet capture file
    print(f"Analyzing {pcap_file}")
    # analyze_rdp_failed_attempts(pcap_file)
    analyze_ssh_failed_attempts(pcap_file)
    # analyze_ftp_failed_attempts(pcap_file)
