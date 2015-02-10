import unittest

from ftpclient import response


class TestResponse(unittest.TestCase):
    def test_build_port_tuple(self):
        status_code = '227 Entering Passive Mode (127,000,000,001,100,10)'
        expected_tuple = ('127.000.000.001', 25610)

        self.assertEqual(response.response_to_port_tuple(status_code),
                         expected_tuple)
