import unittest

# from nose.tools import assert_dict_contains_subset, assert_dict_equal, assert_true

from .mocks import get_free_port, start_mock_server, read_mock_data
from servicenowpy import Client


class TestMockServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mock_server_port = get_free_port()
        start_mock_server(cls.mock_server_port)

    def test_request_response(self):
        mock_instance_url = 'http://localhost:{port}'.format(port=self.mock_server_port)

        sn_client = Client(mock_instance_url, 'user', 'pwd')
        inc_table = sn_client.table('incident')

        url = inc_table.make_url()
        session = inc_table.get_session({"Accept":"application/json"})
        response = session.get(url)

        self.assertDictContainsSubset(
            {'Content-Type': 'application/json;charset=UTF-8'},
            response.headers
        )
        self.assertTrue(response.ok)
        self.assertDictEqual(
            response.json(),
            {"result": read_mock_data()}
        )