from orca import exceptions


class KialiClientException(exceptions.OrcaError):

    message = "Failed to perform a request to Kiali HTTP API: %(reason)s."
