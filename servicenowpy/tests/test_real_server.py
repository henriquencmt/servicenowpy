import os

from unittest import skipIf, TestCase

from servicenowpy import Client


INSTANCE_URL = os.environ['SERVICENOWPY_INSTANCE_URL']
USER = os.environ['SERVICENOWPY_USER']
PASSWORD = os.environ['SERVICENOWPY_PASSWORD']
SKIP_TAGS = os.environ['SERVICENOWPY_SKIP_TAGS']


class TestRealAPI(TestCase):

    @skipIf('real' in SKIP_TAGS, 'Skipping tests that hit the real API server.')
    def test_request_response(self):
        sn_client = Client(INSTANCE_URL, USER, PASSWORD)
        inc_table = sn_client.table('incident')

        url = inc_table.make_url(sysparm_limit=1)
        session = inc_table.get_session({"Accept":"application/json"})
        response = session.get(url)

        self.assertDictContainsSubset({'Content-Type': 'application/json;charset=UTF-8'}, response.headers)
        self.assertRegex(response.headers['Link'], r'(.*),<(.*)>;rel="next')
        self.assertTrue(response.ok)
        self.assertIsInstance(response.json(), dict)