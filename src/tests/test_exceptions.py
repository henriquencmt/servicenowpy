import unittest

from servicenowpy import StatusCodeError
    
class TestExceptions(unittest.TestCase):
    def test_status_code_error_exception(self):
        try:
            raise StatusCodeError('Testing', 'Testing if it raises right', 404)
        except StatusCodeError as e:
            self.assertEqual(e.message, 'Testing')
            self.assertEqual(e.detail, 'Testing if it raises right')
            self.assertEqual(e.status, 404)
