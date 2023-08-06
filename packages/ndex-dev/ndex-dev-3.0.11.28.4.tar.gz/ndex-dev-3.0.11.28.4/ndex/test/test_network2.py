import unittest

import ndex.client as nc
import time
from os import path


ndex_host = "http://dev.ndexbio.org"
ndex_network_resource = "/v2/network/"
username_1 = "cj"
password_1 = "aaa"


class MyTestCase(unittest.TestCase):

    def test_get_network_as_cx_stream(self):
        ndex = nc.Ndex(host=ndex_host, username=username_1, password=password_1)

        network_UUID = "e61d4d09-464f-11e7-96f7-06832d634f41"

        for x in range (0,8000):
            print x
            network_as_cx_stream = ndex.get_network_as_cx_stream(network_UUID)
            network_as_cx = str(network_as_cx_stream.text)

            print len(network_as_cx)

if __name__ == '__main__':
    unittest.main()

