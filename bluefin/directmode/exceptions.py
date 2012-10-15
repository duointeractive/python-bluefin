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
        self.message = self.clean_error_message(message)
        # And if you like it raw...
        self.raw_message = message
        # The HTTP error code returned.
        self.error_code = error_code

    def __str__(self):
        if self.error_code:
            return "%s (Error Code: %s)" % (self.message, self.error_code)
        else:
            return self.message

    def clean_error_message(self, message):
        """
        Some of Bluefin's errors are pretty bad, particularly the reason_code2
        errors. We provide a stub here to make some of the really awful
        error messages more bearable. This is currently only used
        in V3ClientDeclinedException, but may grow with time as more
        hideous errors are encountered.

        :rtype: basestring
        :returns: A 'prettied up' error message.
        """

        return message


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


class V3ClientDeclinedException(V3ClientProcessingException):
    """
    Bluefin has a wonky additional 'status_code' return value that is used
    separately from HTTP status codes. These look to all be authorization
    related so far.
    """

    def clean_error_message(self, message):
        """
        These 'status_code' errors have hideous error messages that just
        aren't good to show users. We'll pretty them up here. Whatever is
        returned here becomes :py:attr:`message`, while the original gets
        set to :py:attr:`raw_message`.

        :rtype: basestring
        """

        if not message:
            # Can't do much here.
            return message

        if message.startswith("CVV2"):
            return "The Card Security Code that was provided is invalid. " \
                   "Please check the three-digit security code on the back of " \
                   "your card and try again."
        elif message.startswith("INVALID CARD NO"):
            return "The credit card number that was provided is invalid. Please "\
                   "re-enter and try again."
        elif message.startswith("CVD"):
            return "Invalid card number, security code, or other value. Please " \
                   "check your input and try again."
        elif message.startswith("C/DECLINED"):
            return "Your payment was declined."
        elif message.startswith("AUTH DECLINED"):
            return "Your payment was declined."

        return message