import os
import unittest

from servicenowpy import Client


class TestMockAPI(unittest.TestCase):
    def test_response(self):
        mock_instance_url = os.environ['SERVICENOWPY_MOCK_API_URL']

        sn_client = Client(mock_instance_url, 'user', 'pwd')
        inc_table = sn_client.table('incident')

        url = inc_table.make_url()
        session = inc_table.get_session({"Accept":"application/json"})
        response = session.get(f'{mock_instance_url}/api/now/table/incident')

        self.assertEqual(
            'application/json;charset=UTF-8',
            response.headers['X-Content-Type']
        )
        self.assertTrue(response.ok)
        self.assertIsInstance(response.content, type(b''))
