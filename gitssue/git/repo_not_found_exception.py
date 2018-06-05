""" Exception for when the local repo can't be found. """


class RepoNotFoundException(Exception):
    """
    Exception for when the local repo can't be found.
    """

    _ERROR_MESSAGE = 'An error occurred - is this a git repository?'

    def __init__(self):
        """
        Superclass constructor call.
        """
        super(RepoNotFoundException, self).__init__(self._ERROR_MESSAGE)
