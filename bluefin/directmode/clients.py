"""
Client classes for Direct Mode services.
"""

import urlparse
import requests

from bluefin.directmode.exceptions import V3ClientInputException, V3ClientProcessingException, V3ClientException, V3ClientDeclinedException

class V3Client(object):
    """
    This is the class used to send API calls and receive responses through for
    the V3.x Direct Mode API client.
    """
    def __init__(self, host='https://secure.bluefingateway.com:1402',
                 path='/gw/sas/direct3.1', http_timeout=15,
                 account_id=None, dynip_sec_code=None):
        """
        Instantiates our API interface with sensible defaults.

        :keyword str host: Full URI to the API gateway, including protocol,
            hostname, and port. No trailing slash.
        :keyword str path: The path to the API endpoint.
        :keyword int http_timeout: Socket timeout in seconds. This is globally
            applied, so be careful.
        :keyword int account_id: Your Bluefin account number. Providing this
            value here means you don't have to pass it with each value dict
            to :py:meth:`send_request`.
        :keyword str dynip_sec_code: A dynamic IP security code. Providing this
            value here means you don't have to pass it with each value dict
            to :py:meth:`send_request`.
        """
        # Default to the HTTPS endpoint.
        self.host = host
        # Default to the Transaction interface.
        self.path = path
        # Note that this is applied gobally, so be careful.
        self.http_timeout = http_timeout

        self.default_values = {}

        if account_id:
            self.default_values['account_id'] = account_id
        if dynip_sec_code:
            self.default_values['dynip_sec_code'] = dynip_sec_code

    def _get_endpoint(self):
        """
        urllib2.Request wants a full URI with protocol, host, and path.
        Assemble the proto+host+path into a URI to request.
        """
        return '%s%s' % (self.host, self.path)

    def _check_for_error_http_status_code(self, response):
        """
        Checks the response's HTTP status code for common error code numbers.

        :param requests.Response response: A requests Response object generated
            by requests.post().
        :raises: An appropriate bluefin.directmode.exceptions.V3ClientException
            sub-class, depending on the error.
        """
        http_status = response.status_code

        if http_status >= 600 and http_status <= 699:
            # HTTP error codes 600-699 are input errors.
            raise V3ClientInputException(response.text, error_code=http_status)
        elif http_status >= 700 and http_status <= 799:
            # HTTP error codes 700-799 http_status processing errors.
            raise V3ClientProcessingException(response.text, error_code=http_status)
        elif http_status > 200:
            raise V3ClientException(response.text, error_code=http_status)

    def _check_parsed_response_for_error_codes(self, result_dict):
        """
        Looks through the dict that we get by parsing the response from Bluefin.
        Finds any known error conditions, raises an appropriate exception.

        :param dict result_dict: The urlparsed response from Bluefin.
        :raises: An appropriate bluefin.directmode.exceptions.V3ClientException
            sub-class, depending on the error.
        """

        status_code = result_dict.get('status_code')
        # These are the two status codes that indicate issues.
        if result_dict.get('status_code') in ['F', '0']:
            reason_code = result_dict.get('reason_code2')
            # There are multiple error fields to check. auth_msg is almost always
            # the one to go by.
            err_message = result_dict.get('auth_msg') or reason_code
            # These errors don't tend to use HTTP status codes, so check the
            # reason_code2 field.
            exc_code = status_code or reason_code
            raise V3ClientDeclinedException(err_message, error_code=exc_code)

    def send_request(self, values):
        """
        Sends an API request. You are on your own to pass in the correct
        key/value pairs as a dict in the ``values`` argument.

        :param dict values: Key/value pairs for your desired API call. See
            the Bluefin documentation for what these should be.
        :rtype: dict
        :returns: A dict of output from the API server. See the Bluefin API
            docs for how to interpret this.
        :raises: V3ClientInputException when the Bluefin API says we have
            an input error, and V3ClientProcessingException when the Bluefin
            API encounters an error during processing. The lower level
            urllib2 may raise urllib2.HTTPError exceptions also.
        """

        # Copy the default values dict so we don't have to repeat stuff like
        # account_id and dynip_sec_code for every request.
        all_values = self.default_values.copy()
        # The transaction values can override the defaults.
        all_values.update(values)

        response = requests.post(
            self._get_endpoint(),
            data=all_values,
            timeout=self.http_timeout
        )
        # Looks at the HTTP status code and raises an exception if any of the
        # known number ranges for errors are returned.
        self._check_for_error_http_status_code(response)

        result_dict = urlparse.parse_qs(response.text)
        for key, value in result_dict.items():
            # Strip away the lists from the value, since these should all just
            # be a one-member list. We'll join with commas just in case.
            result_dict[key] = ','.join(value)

        # Looks through the parsed response dict for common error codes. Raises
        # exceptions if any are found.
        self._check_parsed_response_for_error_codes(result_dict)

        return result_dict