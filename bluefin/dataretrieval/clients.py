"""
Client classes for Data Retrieval Interface API.
"""
import socket
import urllib
import urllib2
import urlparse
import requests

from bluefin.dataretrieval.exceptions import V1ClientProcessingException, V1ClientInputException, V1ClientException

class V1Client(object):
    """
    This is the class used to send API calls and receive responses through for
    the V1.x Data Retrival Interface API client.
    """
    def __init__(self, host='https://secure.bluefingateway.com',
                 path='/gw/reports/transaction1.5', http_timeout=15):
        """
        Instantiates our API interface with sensible defaults.

        :keyword str host: Full URI to the API gateway, including protocol,
            hostname, and port. No trailing slash.
        :keyword str path: The path to the API endpoint.
        :keyword int http_timeout: Socket timeout in seconds. This is globally
            applied, so be careful.
        """
        # Default to the HTTPS endpoint.
        self.host = host
        # Default to the Transaction interface.
        self.path = path
        # Note that this is applied gobally, so be careful.
        self.http_timeout = http_timeout

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

        if http_status >= 457:
            # HTTP error codes 600-699 are input errors.
            raise V1ClientInputException(response.text, error_code=http_status)
        elif http_status > 417 and http_status < 500:
            # HTTP error codes 700-799 http_status processing errors.
            raise V1ClientProcessingException(response.text, error_code=http_status)
        elif http_status > 200:
            raise V1ClientException(response.text, error_code=http_status)

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

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'secure.bluefingateway.com',
            'User-Agent': 'PythonBluefin/Version:2011.Jun.28',
        }

        response = requests.post(
            self._get_endpoint(),
            data=values,
            headers=headers,
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

        return result_dict