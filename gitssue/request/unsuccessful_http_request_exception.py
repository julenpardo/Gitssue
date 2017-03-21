""" Exception for when the request code is not 200. """


class UnsuccessfulHttpRequestException(Exception):
    """
    Exception for when the request code is not 200. The request code and headers
    are also saved, because each remote (Github, Gitlab, etc.) may handle "special"
    unsuccessful requests in different ways. For example, for Github, when the
    API request limit is reached, a 403 code is returned, so we should look for the
    'X-RateLimit' headers, to know that exactly is a rate limit error.
    """

    def __init__(self, code, headers):
        """
        Constructor.
        :param code: The error code for the request.
        :param headers: The headers sent for the error request.
        """
        super(UnsuccessfulHttpRequestException, self).__init__()
        self.code = code
        self.headers = headers
