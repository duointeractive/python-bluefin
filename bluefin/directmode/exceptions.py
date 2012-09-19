"""
Exception classes for Direct Mode API operations.
"""
class V3ClientException(Exception):
    """
    Used to denote some kind of generic error. This does not include errors
    returned from Bluefin API responses. Those are handled by the more
    specific exception classes below.
    """
    def __init__(self, message, error_code=None, *args):
        Exception.__init__(self, message, error_code, *args)
        # The error message back from the Bluefin API server.
        self.message = message
        # The HTTP error code returned.
        self.error_code = error_code

    def __str__(self):
        if self.error_code:
            return "%s (Error Code: %s)" % (self.message, self.error_code)
        else:
            return self.message


class V3ClientInputException(V3ClientException):
    """
    Raised when HTTP error codes 600-699 are returned, indicating an input
    issue of some sort.
    """
    pass


class V3ClientProcessingException(V3ClientException):
    """
    Raised when a processing error occurs on the Bluefin side. These are
    generally HTTP error codes 700-799.
    """
    pass