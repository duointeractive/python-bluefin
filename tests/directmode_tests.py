import unittest
from bluefin.directmode.clients import V3Client
from bluefin.directmode.exceptions import V3ClientInputException
from tests.api_details import API_DETAILS, TEST_CARD

class SaleTests(unittest.TestCase):
    """
    Tests for the 'sale' transaction type.
    """
    def setUp(self):
        self.api = V3Client()

    def test_basic(self):
        """
        Test a basic successful API call.
        """
        response = self.api.send_request({
            'pay_type': 'C',
            'tran_type': 'S',
            'account_id': API_DETAILS['account_id'],
            'amount': 1.0,
            'card_number': TEST_CARD['card_number'],
            'card_expire': TEST_CARD['card_expire'],
            'dynip_sec_code': API_DETAILS['dynip_sec_code'],
            # Must be the customer's IP address.
            'cust_ip': '127.0.0.1',
            'bill_name1': 'First',
            'bill_name2': 'Last',
            'bill_street': '123 Some Street',
            'bill_zip': '12345',
            # Two-letter country code.
            # http://www.iso.org/iso/en/prods-services/iso3166ma/index.html
            'bill_country': 'US',
        })
        self.assertEqual(response['status_code'], '1')


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
            # Must be the customer's IP address.
            'cust_ip': '127.0.0.1',
            'bill_name1': 'First',
            'bill_name2': 'Last',
            'bill_street': '123 Some Street',
            'bill_zip': '12345',
            # Two-letter country code.
            # http://www.iso.org/iso/en/prods-services/iso3166ma/index.html
            'bill_country': 'US',
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