class OrcaError(Exception):

    message = "An unknown exception occurred."

    def __init__(self, **kwargs):
        msg = self.message % kwargs
        super(OrcaError, self).__init__(msg)
