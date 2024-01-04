'''
testing for portScan.py
'''
import unittest
import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.append(parent_dir)
import portScan

#not implemented yet

class TestPortScan(unittest.TestCase):
    file1='./testPCAPs/3-ericka.pcapng'
    file2='./testPCAPs/3-ericka.pcapng'
    file3='./testPCAPs/5-evil.pcapng'
    file4='./testPCAPs/udpPortScanSuccess.pcapng'
    file5='./testPCAPs/synPortScanSuccess.pcapng'
    files = [file1,file2,file3,file4,file5]
    ans1 = []
    ans2 = []
    ans3 = []
    ans4 = []
    ans5 = []
    ans = [ans1,ans2,ans3,ans4,ans5]

    def test_analyze_udp_port_scan(self):
        pass
        for index,file in enumerate(self.files):
            self.assertEqual(portScan.analyze_udp_port_scan(file), self.ans[index])
        return "test_analyze_udp_port_scan passed"

    def test_analyze_syn_port_scan(self):
        pass
        for index,file in enumerate(self.files):
            self.assertEqual(portScan.analyze_syn_port_scan(file), self.ans[index])
        return "test_analyze_syn_port_scan passed"

if __name__ == '__main__':
    tests = TestPortScan()
    tests.test_analyze_udp_port_scan()
    tests.test_analyze_syn_port_scan()