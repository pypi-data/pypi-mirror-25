'''
Test communicationguru
'''
import unittest
from communicationguru import CommunicationGuru

GURU_URL = 'https://communicationguru.appointmentguru.co'

class TestCommunicationGuruTestCase(unittest.TestCase):

    def setUp(self):
        self.comms = CommunicationGuru(GURU_URL)

    def test_send_email(self):
        res = self.comms.send_email(['info@38.co.za'], 'testing', 'this is a test')


    def test_send_sms(self):
        res = self.comms.send_sms('this is a test', '+27832566533')

if __name__ == '__main__':
    unittest.main()

