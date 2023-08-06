from requests.exceptions import HTTPError


class FieldawareError(HTTPError):
    """Generic error while attempting to communicate with Fieldaware"""

class UnknownStatusCode(FieldawareError):
    """Status code has not been added to system"""

class APIValidationError(FieldawareError):
    """
        (422)
        The query parameters and/or body is not valid for this request.
        This error captures violation of structural assumptions made on the
        inputs, as captured by the different schemas that are included in the
        Reference section of this documentation.
    """

class ConflictError(FieldawareError):
    """
        (409)
        The server cannot satisfy an otherwise valid request because of a
        conflicting business logic rule (e.g. attempting to invoice a
        non-completed job). While an APIValidationError will never be
        acceptable if re-submitted, a request that gives rise to a
        ConflictError may be acceptable after other resource state changes
        (e.g. a job is completed by a field engineer).

    """

class AuthenticationError(FieldawareError):
    """"
        (401)
        The client failed to authenticate, typically because the API token was
        either invalid or not included in the request.
    """

class NotFoundError(FieldawareError):
    """"
        (404)
        A specified resource does not exist. This may be the top-level
        resource at which the request was directed, but it may also be one of
        the entities referenced in the payload. The error message should
        contain the exact reference that caused offence.
    """


class BadRequest(FieldawareError):
    """
        (400)
        The payload is syntactically malformed. For example, the inputs are
        not encoded as JSON, or the payload is not valid JSON.
    """

class APIKeyMissingError(Exception):
    pass


class UUIDMissingError(Exception):
    pass


class InvalidObjectType(Exception):
    pass
