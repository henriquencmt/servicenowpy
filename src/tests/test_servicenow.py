import unittest

import requests

from .mocks import get_free_port, start_mock_server, read_mock_data
from servicenowpy import Client, Table, StatusCodeError

class TestClient(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.sn_client = Client('instance_url', 'user', 'pwd')

    def test_make_api_url_without_protocol(self):
        api_url = self.sn_client.make_api_url('mock.service-now.com')
        expected = 'https://mock.service-now.com/api/now/'
        self.assertEqual(api_url, expected)

    def test_make_api_url_with_https(self):
        api_url = self.sn_client.make_api_url('https://mock.service-now.com')
        expected = 'https://mock.service-now.com/api/now/'
        self.assertEqual(api_url, expected)

    def test_make_api_url_with_http(self):
        api_url = self.sn_client.make_api_url('http://mock.service-now.com')
        expected = 'http://mock.service-now.com/api/now/'
        self.assertEqual(api_url, expected)

    def test_table(self):
        inc_table = self.sn_client.table('incident')
        self.assertIsInstance(inc_table, Table)


class TestTable(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mock_server_port = get_free_port()
        start_mock_server(cls.mock_server_port)

        cls.mock_instance_url = 'http://localhost:{port}/'.format(port=cls.mock_server_port)

        cls.inc_table = Table('incident', cls.mock_instance_url, ('user', 'pwd'))

        cls.bad_table = Table('badtable', cls.mock_instance_url, ('user', 'pwd'))

    def test_get(self):
        result = self.inc_table.get()
        self.assertEqual(result, read_mock_data())
    
    def test_get_with_query(self):
        result = self.inc_table.get(sysparm_fields='number,assignment_group')
        self.assertEqual(result, read_mock_data())

    def test_get_record(self):
        sys_id = '001'
        result = self.inc_table.get_record(sys_id)
        self.assertEqual(result, read_mock_data(single_record=True))

    def test_get_record_by_number(self):
        number = 'INC0000060'
        result = self.inc_table.get_record_by_number(number)
        self.assertEqual(result[0], read_mock_data(single_record=True))

    def test_patch(self):
        pass

    def test_post(self):
        number = 'INC0000060'
        result = self.inc_table.post()
        self.assertEqual(result[0], read_mock_data(single_record=True))

    def test_put(self):
        pass

    def test_delete(self):
        pass

    def test_get_session(self):
        headers = {"Accept":"application/json"}
        inc_table = Table('incident', 'instance', ())
        session = inc_table.get_session(headers)
        self.assertIsInstance(session, requests.Session)
        self.assertDictContainsSubset({"Accept":"application/json"}, session.headers)

    def test_check_status_code_raises_exception(self):
        self.assertRaises(StatusCodeError, self.bad_table.get)

    def test_make_url(self):
        pass
        