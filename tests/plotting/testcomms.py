import json
from nose.plugins.attrib import attr
from holoviews.element.comparison import ComparisonTestCase
from holoviews.plotting.comms import Comm, JupyterComm


class TestComm(ComparisonTestCase):

    def test_init_comm(self):
        Comm()

    def test_init_comm_id(self):
        comm = Comm(id='Test')
        self.assertEqual(comm.id, 'Test')

    def test_decode(self):
        msg = 'Test'
        self.assertEqual(Comm.decode(msg), msg)

    def test_handle_message_error_reply(self):
        def raise_error(msg):
            raise Exception('Test')
        def assert_error(msg):
            decoded = json.loads(msg)
            self.assertEqual(decoded['msg_type'], "Error")
            self.assertTrue(decoded['traceback'].endswith('Exception: Test'))
        comm = Comm(id='Test', on_msg=raise_error)
        comm.send = assert_error
        comm._handle_msg({})

    def test_handle_message_ready_reply(self):
        def assert_ready(msg):
            self.assertEqual(json.loads(msg), {'msg_type': "Ready", 'content': ''})
        comm = Comm(id='Test')
        comm.send = assert_ready
        comm._handle_msg({})

    def test_handle_message_ready_reply_with_comm_id(self):
        def assert_ready(msg):
            decoded = json.loads(msg)
            self.assertEqual(decoded, {'msg_type': "Ready", 'content': '',
                                       'comm_id': 'Testing id'})
        comm = Comm(id='Test')
        comm.send = assert_ready
        comm._handle_msg({'comm_id': 'Testing id'})


@attr(optional=1)
class TestJupyterComm(ComparisonTestCase):

    def test_init_comm(self):
        JupyterComm()

    def test_init_comm_id(self):
        comm = JupyterComm(id='Test')
        self.assertEqual(comm.id, 'Test')

    def test_decode(self):
        msg = {'content': {'data': 'Test'}}
        decoded = JupyterComm.decode(msg)
        self.assertEqual(decoded, 'Test')

    def test_on_msg(self):
        def raise_error(msg):
            if msg == 'Error':
                raise Exception()
        comm = JupyterComm(id='Test', on_msg=raise_error)
        with self.assertRaises(Exception):
            comm._handle_msg({'content': {'data': 'Error'}})
