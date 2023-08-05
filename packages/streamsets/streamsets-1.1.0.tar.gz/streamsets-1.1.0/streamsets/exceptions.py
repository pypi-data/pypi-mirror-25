# Copyright 2017 StreamSets Inc.

"""Common exceptions."""


class InternalServerError(Exception):
    """Internal server error."""
    def __init__(self, response):
        self.status_code = response.status_code
        self.response = response.json()
        self.text = self.response['RemoteException']['localizedMessage']

        # Propagate message from the REST interface as message of the exception
        super().__init__(self.text)


class ActivationError(Exception):
    """Activation error."""
    def __init__(self, reason=None):
        self.reason = reason

    def __str__(self):
        return ('Failed to activate Python SDK '
                'for StreamSets ({}).'.format('reason: {}'.format(self.reason)
                                              if self.reason
                                              else 'no reason provided'))
