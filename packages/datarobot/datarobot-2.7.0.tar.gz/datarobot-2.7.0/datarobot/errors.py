import warnings


class AppPlatformError(Exception):
    """
    Raised by :meth:`Client.request()` for requests that:
      - Return a non-200 HTTP response, or
      - Connection refused/timeout or
      - Response timeout or
      - Malformed request
      - Have a malformed/missing header in the response.
    """
    def __init__(self, exc_message, status_code, error_code=None):
        super(AppPlatformError, self).__init__(exc_message)
        self.status_code = status_code
        self.error_code = error_code


class ServerError(AppPlatformError):
    """
    For 500-level responses from the server
    """


class ClientError(AppPlatformError):
    """
    For 400-level responses from the server
    """


class InputNotUnderstoodError(Exception):
    """
    Raised if a method is called in a way that cannot be understood
    """


class AllRetriesFailedError(Exception):
    """Raised when the retry manager does not successfully make a request"""


class InvalidModelCategoryError(Exception):
    """
    Raised when method specific for model category was called from wrong model
    """


class AsyncTimeoutError(Exception):
    """
    Raised when an asynchronous operation did not successfully get resolved
    within a specified time limit
    """


class AsyncFailureError(Exception):
    """
    Raised when querying an asynchronous status resulted in an exceptional
    status code (not 200 and not 303)
    """


class ProjectAsyncFailureError(AsyncFailureError):
    """
    When an AsyncFailureError occurs during project creation or finalizing the project
    settings for modeling. This exception will have the attributes ``status_code``
    indicating the unexpected status code from the server, and ``async_location`` indicating
    which asynchronous status object was being polled when the failure happened.
    """
    def __init__(self, exc_message, status_code, async_location):
        super(ProjectAsyncFailureError, self).__init__(exc_message)
        self.status_code = status_code
        self.async_location = async_location


class AsyncProcessUnsuccessfulError(Exception):
    """
    Raised when querying an asynchronous status showed that async process
    was not successful
    """


class AsyncModelCreationError(Exception):
    """
    Raised when querying an asynchronous status showed that model creation
    was not successful
    """


class AsyncPredictionsGenerationError(Exception):
    """
    Raised when querying an asynchronous status showed that predictions
    generation was not successful
    """


class PendingJobFinished(Exception):
    """
    Raised when the server responds with a 303 for the pending creation of a
    resource.
    """


class JobNotFinished(Exception):
    """
    Raised when execution was trying to get a finished resource from a pending
    job, but the job is not finished
    """


class DuplicateFeaturesError(Exception):
    """
    Raised when trying to create featurelist with duplicating features
    """


class DataRobotDeprecationWarning(DeprecationWarning):
    """
    Raised when using deprecated functions or using functions in a deprecated way
    """
    pass


class IllegalFileName(Exception):
    """
    Raised when trying to use a filename we can't handle.
    """


class JobAlreadyRequested(ClientError):
    """
    Raised when the requested model has already been requested.
    """

warnings.filterwarnings('default', category=DataRobotDeprecationWarning)
