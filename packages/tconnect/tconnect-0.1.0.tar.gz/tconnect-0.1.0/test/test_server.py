from thrift_test import TestService
from test_service import TestServiceImpl
from tconnect import TServer
from multiprocessing import Process
from thrift.transport.TSocket import TSocket
import time

TEST_PORT = 9101


class TestServer:

    def test_connection(self, _protocol, _transport):
        server = TServer(TEST_PORT, TestService, TestServiceImpl(), _protocol[1], _transport[1])
        process = Process(target=server.serve)
        process.start()
        time.sleep(5)

        # connect with client
        socket = TSocket('localhost', TEST_PORT)
        transport = _transport[0](socket)
        transport.open()
        protocol = _protocol[0](transport)
        client = TestService.Client(protocol)

        # perform test
        assert client.alive()

        # cleanup
        transport.close()
        process.terminate()

