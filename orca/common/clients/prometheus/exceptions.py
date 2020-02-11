from orca import exceptions


class PrometheusClientException(exceptions.OrcaError):

    message = "Failed to perform a request to Prometheus HTTP API: %(reason)s."
