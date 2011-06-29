"""
Client classes for Data Retrieval Interface API.
"""
import socket
import urllib
import urllib2
import urlparse

from bluefin.dataretrieval.exceptions import V1ClientProcessingException, V1ClientInputException

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
        # This is applied globally!
        socket.setdefaulttimeout(self.http_timeout)

        data = urllib.urlencode(values)

        headers = {
            'Content-Length': len(data),
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'secure.bluefingateway.com',
            'User-Agent': 'PythonBluefin/Version:2011.Jun.28',
        }

        request = urllib2.Request(self._get_endpoint(), data, headers)
        try:
            result = urllib2.urlopen(request).read()
        except urllib2.HTTPError, exc:
            error_code = exc.getcode()

            if error_code == 457:
                raise V1ClientInputException(exc.msg, error_code=error_code)
            elif error_code > 417 and error_code < 500:
                raise V1ClientProcessingException(exc.msg, error_code=error_code)
            else:
                raise

        result_dict = urlparse.parse_qs(result)
        for key, value in result_dict.items():
            # Strip away the lists from the value, since these should all just
            # be a one-member list. We'll join with commas just in case.
            result_dict[key] = ','.join(value)

        return result_dict