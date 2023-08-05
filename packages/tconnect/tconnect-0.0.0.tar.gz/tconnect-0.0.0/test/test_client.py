from thrift.transport.TSocket import TServerSocket
from thrift.transport.TTransport import TFramedTransportFactory
from thrift.protocol.TCompactProtocol import TCompactProtocolAcceleratedFactory
from thrift.server.TServer import TSimpleServer
from thrift_test import TestService
from test_service import TestServiceImpl
from multiprocessing import Process
from tconnect import TClient
import time

TEST_PORT = 9102


class TestClient:

    def test_connection(self, _protocol, _transport):
        socket = TServerSocket(port=TEST_PORT)
        processor = TestService.Processor(TestServiceImpl())
        server = TSimpleServer(processor, socket, _transport[1](), _protocol[1]())
        process = Process(target=server.serve)
        process.start()
        time.sleep(5)

        # connect with client
        client = TClient('localhost', TEST_PORT, TestService, 30000, _protocol[0], _transport[0])

        # perform test
        assert client.alive()

        # cleanup
        process.terminate()

