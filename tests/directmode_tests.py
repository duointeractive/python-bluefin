import unittest
from bluefin.directmode.clients import V3Client
from bluefin.directmode.exceptions import V3ClientInputException
from tests.api_details import API_DETAILS, TEST_CARD

class AuthorizeTests(unittest.TestCase):
    """
    Tests for authorization API calls.
    """
    def setUp(self):
        self.api = V3Client()

    def test_basic(self):
        """
        Test a basic successful API call.
        """
        self.api.send_request({
            'pay_type': 'C',
            'tran_type': 'A',
            'account_id': API_DETAILS['account_id'],
            'amount': 1.0,
            'card_number': TEST_CARD['card_number'],
            'card_expire': TEST_CARD['card_expire'],
            'dynip_sec_code': API_DETAILS['dynip_sec_code'],
        })

    def test_invalid_sec_code(self):
        """
        Use an invalid security code to test exception handling.
        """
        api_values = {
            'pay_type': 'C',
            'tran_type': 'A',
            'account_id': API_DETAILS['account_id'],
            'amount': 1.0,
            'card_number': TEST_CARD['card_number'],
            'card_expire': TEST_CARD['card_expire'],
            'dynip_sec_code': 'HUZZAH_FOR_I_AM_INVALID',
        }

        self.assertRaises(V3ClientInputException, self.api.send_request, api_values)


    def test_missing_cc_num(self):
        api_values = {
            'pay_type': 'C',
            'tran_type': 'A',
            'account_id': API_DETAILS['account_id'],
            'amount': 1.0,
            #'card_number': TEST_CARD['card_number'],
            'card_expire': TEST_CARD['card_expire'],
            'dynip_sec_code': API_DETAILS['dynip_sec_code'],
            }

        self.assertRaises(V3ClientInputException, self.api.send_request,
                          api_values)

    def test_missing_cc_expiration(self):
        api_values = {
            'pay_type': 'C',
            'tran_type': 'A',
            'account_id': API_DETAILS['account_id'],
            'amount': 1.0,
            'card_number': TEST_CARD['card_number'],
            #'card_expire': TEST_CARD['card_expire'],
            'dynip_sec_code': API_DETAILS['dynip_sec_code'],
            }

        self.assertRaises(V3ClientInputException, self.api.send_request,
                          api_values)

    def test_missing_amount(self):
        api_values = {
            'pay_type': 'C',
            'tran_type': 'A',
            'account_id': API_DETAILS['account_id'],
            #'amount': 1.0,
            'card_number': TEST_CARD['card_number'],
            'card_expire': TEST_CARD['card_expire'],
            'dynip_sec_code': API_DETAILS['dynip_sec_code'],
            }

        self.assertRaises(V3ClientInputException, self.api.send_request,
                          api_values)

    def test_invalid_amount(self):
        api_values = {
            'pay_type': 'C',
            'tran_type': 'A',
            'account_id': API_DETAILS['account_id'],
            'amount': -1.0,
            'card_number': TEST_CARD['card_number'],
            'card_expire': TEST_CARD['card_expire'],
            'dynip_sec_code': API_DETAILS['dynip_sec_code'],
            }

        self.assertRaises(V3ClientInputException, self.api.send_request,
                          api_values)

        # Now set it to something non-numerical.
        api_values['amount'] = 'a'
        self.assertRaises(V3ClientInputException, self.api.send_request,
                          api_values)

class AuthorizeRecurringTests(unittest.TestCase):
    """
    Unit tests for recurring payment authorization.
    """
    def setUp(self):
        self.api = V3Client()

    def test_basic(self):
        """
        Test a basic successful API call.
        """
        self.api.send_request({
            'pay_type': 'C',
            'tran_type': 'A',
            'account_id': API_DETAILS['account_id'],
            'amount': 1.0,
            'recurring_amount': 1.0,
            'recurring_period': 31,
            'card_number': TEST_CARD['card_number'],
            'card_expire': TEST_CARD['card_expire'],
            'dynip_sec_code': API_DETAILS['dynip_sec_code'],
            })