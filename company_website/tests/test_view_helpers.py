from unittest import TestCase
from unittest.mock import Mock
from unittest.mock import patch

from requests.exceptions import Timeout

from company_website.view_helpers import generate_subresource_integrity_sha384
from company_website.view_helpers import REQUESTS_TIMOUT


def mocked_requests(_url, timeout):  # pylint: disable=unused-argument
    obj = Mock()
    obj.content = b"ffuffuffufristajlo"
    return obj


class ViewHelpersTests(TestCase):
    def setUp(self):
        self.url = "http://script-resource-address.com"

    @patch("company_website.view_helpers.requests.get", side_effect=mocked_requests)
    def test_generate_subresource_integrity_sha384_return_correct_hash(self, request_mock):
        sha384 = generate_subresource_integrity_sha384(self.url)
        self.assertEqual(sha384, "sha384-V8nQQcxIliIrOeLNsdHU/J3LkCORHKeOhUY5aqyK+f8iKihsQnd9ebM58ei/Cttm")
        request_mock.assert_called_with(self.url, timeout=REQUESTS_TIMOUT)

    @patch("company_website.view_helpers.requests")
    def test_generate_subresource_integrity_sha384_return_empty_string_when_timeout(self, mock_requests):
        mock_requests.get.side_effect = Timeout
        sha384 = generate_subresource_integrity_sha384(self.url)
        self.assertEqual(sha384, "")
