from orca import exceptions


class APIClientError(exceptions.OrcaError):

    message = "Failed to perform API request: %(reason)s."
