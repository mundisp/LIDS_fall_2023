'''
testing for loginAttempt.py
'''
import unittest
import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.append(parent_dir)
import loginAttempt

class TestLoginAttempt(unittest.TestCase):
    file1='./samplePCAPs/3-ericka.pcapng'
    file2='./samplePCAPs/3-ericka.pcapng'
    file3='./samplePCAPs/5-evil.pcapng'
    file4='./samplePCAPs/udpPortScanSuccess.pcapng'
    file5='./samplePCAPs/synPortScanSuccess.pcapng'
    files = [file1,file2,file3,file4,file5]
    ssh_ans = [{'10.0.0.5*10.0.0.3': 3}, {'10.0.0.5*10.0.0.3': 3}, {'10.0.0.5*10.0.0.3': 3}, {}, {}]
    ftp_ans = [{'10.0.0.5*10.0.0.3': 2}, {'10.0.0.5*10.0.0.3': 2}, {'10.0.0.5*10.0.0.3': 2}, {}, {}]
    rdp_ans = [{'10.0.0.5*10.0.0.3*3389': 3}, {'10.0.0.5*10.0.0.3*3389': 3}, {'10.0.0.5*10.0.0.3*3389': 3}, {}, {}]

    def test_analyze_ssh_failed_attempts(self):
        for index,file in enumerate(self.files):
            self.assertEquals(loginAttempt.analyze_ssh_failed_attempts(file), self.ssh_ans[index])
        return "test_analyze_ssh_failed_attempts passed"
    
    def test_analyze_ftp_failed_attempts(self):
        for index,file in enumerate(self.files):
            self.assertEqual(loginAttempt.analyze_ftp_failed_attempts(file), self.ftp_ans[index])
        return "test_analyze_ftp_failed_attempts passed"

    def test_analyze_rdp_failed_attempts(self):
        for index,file in enumerate(self.files):
            self.assertEqual(loginAttempt.analyze_rdp_failed_attempts(file), self.rdp_ans[index])
        return "test_analyze_rdp_failed_attempts passed"

if __name__ == '__main__':
    tests = TestLoginAttempt()
    results=[]
    results.append(tests.test_analyze_ssh_failed_attempts())
    results.append(tests.test_analyze_ftp_failed_attempts())
    results.append(tests.test_analyze_rdp_failed_attempts())
    print()
    for r in results:
        print(r)
    print()