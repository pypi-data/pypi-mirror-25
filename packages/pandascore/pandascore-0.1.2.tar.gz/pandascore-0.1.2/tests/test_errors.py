import unittest
try:
    from mock import Mock
except ImportError:
    from unittest.mock import Mock

from pandascore.errors import (
    check_status,
    NotFoundError,
    UnauthorizedError,
    MalformedRequestError,
    ForbiddenError,
    UnprocessableError
)

class TestUtils(unittest.TestCase):

    def setUp(self):
        self.mockresult = Mock()
        self.mockresult.url = 'http://www.test.com/'
        self.mockresult.json.return_value = 'test'
        self.mockresult.content = 'test'

    def test_malformed_request(self):
        """Test malformed request (400 code)"""
        self.mockresult.status_code = 400
        with self.assertRaises(MalformedRequestError) as error:
            check_status(200, self.mockresult)

        self.assertEqual(str(error.exception), ('[400]resp: test'))

    def test_not_found(self):
        """Test not found (404 code)"""
        self.mockresult.status_code = 404
        with self.assertRaises(NotFoundError) as error:
            check_status(200, self.mockresult)

        self.assertEqual(str(error.exception), ('[404]resp: test'))

    def test_unauthorized(self):
        """Test a unauthorized (401 code)"""
        self.mockresult.status_code = 401
        with self.assertRaises(UnauthorizedError) as error:
            check_status(200, self.mockresult)

        self.assertEqual(str(error.exception), ('[401]resp: test'))

    def test_forbidden(self):
        """Test a forbidden (403 code)"""
        self.mockresult.status_code = 403
        with self.assertRaises(ForbiddenError) as error:
            check_status(200, self.mockresult)

        self.assertEqual(str(error.exception), ('[403]resp: test'))

    def test_unprocessable(self):
        """Test a unprocessable (422 code)"""
        self.mockresult.status_code = 422
        with self.assertRaises(UnprocessableError) as error:
            check_status(200, self.mockresult)

        self.assertEqual(str(error.exception), ('[422]resp: test'))
