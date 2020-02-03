class OrcaError(Exception):

    message = "An unknown exception occurred."

    def __init__(self, **kwargs):
        msg = self.message % kwargs
        super(OrcaError, self).__init__(msg)


class MappingNotFound(OrcaError):

    message = "Mapping not found for key: %(key)s."
