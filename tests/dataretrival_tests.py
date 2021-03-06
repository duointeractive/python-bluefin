import unittest
from bluefin.dataretrieval.clients import V1Client
from bluefin.dataretrieval.exceptions import V1ClientInputException, V1ClientProcessingException
from tests.api_details import API_DETAILS, TEST_CARD

class TransactionReportingTest(unittest.TestCase):
    """
    Tests for transaction reporting API calls.
    """
    def test_basic(self):
        """
        Test a basic successful API call.
        """
        api = V1Client()
        result = api.send_request({
            'transactions_after': '2006-12-30',
            'account_id': API_DETAILS['account_id'],
            'site_tag': 'MAIN',
            'authorization': API_DETAILS['site_tag_auth_code'],
        })

    def test_no_input(self):

        api = V1Client()
        self.assertRaises(V1ClientInputException, api.send_request, {})


