import json
import os
import unittest

import requests

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
        cls.mock_instance_url = os.environ['SERVICENOWPY_MOCK_API_URL']
        cls.sn_client = Client(cls.mock_instance_url, 'user', 'pwd')


    def test_get(self):
        inc_table = self.sn_client.table('incident')
        result = inc_table.get()
        self.assertIsInstance(result, list)


    def test_get_with_query(self):
        inc_table = self.sn_client.table('incident')
        fields = 'number,assignment_group'
        result = inc_table.get(sysparm_fields=fields)

        self.assertIsInstance(result, list)
        self.assertEqual(
            ','.join(result[0].keys()),
            fields
        )


    def test_get_record(self):
        sys_id = '1c741bd70b2322007518478d83673af3'
        inc_table = self.sn_client.table('incident')
        result = inc_table.get_record(sys_id)
        self.assertIsInstance(result, dict)
        self.assertEqual(result['sys_id'], sys_id)


    def test_get_record_by_number(self):
        number = 'INC0000001'
        inc_table = self.sn_client.table('incident')
        result = inc_table.get_record_by_number(number, verbose=True)
        self.assertIsInstance(result, list)
        self.assertEqual(result[0]['number'], number)


    def test_patch(self):
        sys_id = '1c741bd70b2322007518478d83673af3'
        data = { "assignment_group": "287ebd7da9fe198100f92cc8d1d2154e" }
        inc_table = self.sn_client.table('incident')
        result = inc_table.patch(sys_id, data)

        self.assertIsInstance(result, dict)
        self.assertEqual(result['sys_id'], sys_id)
        self.assertEqual(result['assignment_group'], data['assignment_group'])


    def test_post(self):
        data = { "assignment_group": "287ebd7da9fe198100f92cc8d1d2154e" }
        inc_table = self.sn_client.table('incident')
        result = inc_table.post(data)

        self.assertIsInstance(result, dict)
        self.assertEqual(result['assignment_group'], data['assignment_group'])


    def test_put(self):
        sys_id = '1c741bd70b2322007518478d83673af3'
        data = { "short_description": "Unable to access email" }
        inc_table = self.sn_client.table('incident')
        result = inc_table.put(sys_id, data)

        self.assertIsInstance(result, dict)
        self.assertEqual(result['short_description'], data['short_description'])


    def test_delete(self):
        sys_id = '1c741bd70b2322007518478d83673af3'
        inc_table = self.sn_client.table('incident')
        result = inc_table.delete(sys_id)
        self.assertEqual(result, b'')


    def test_get_session(self):
        headers = {"Accept":"application/json"}
        sn_client = Client('instance.service-now.com', 'user', 'pwd')
        inc_table = sn_client.table('incident')
        session = inc_table.get_session(headers)

        self.assertIsInstance(session, requests.Session)
        self.assertDictContainsSubset({"Accept":"application/json"}, session.headers)


    def test_check_status_code_raises_exception(self):
        bad_table = self.sn_client.table('badtable')
        self.assertRaises(StatusCodeError, bad_table.get)


    def test_make_url(self):
        inc_table = self.sn_client.table('incident')
        url = inc_table.make_url()
        expected = f"{os.environ['SERVICENOWPY_MOCK_API_URL']}/api/now/table/incident"
        self.assertEqual(url, expected)