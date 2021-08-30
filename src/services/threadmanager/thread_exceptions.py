class GeneralError(Exception):
    """Base Exception class for threadmanager"""
    pass


class BadStateError(GeneralError):
    """State is not as expected"""
    pass


class CancelledError(GeneralError):
    """The item being waited on was cancelled"""
    pass


class StopNotificationWarning(UserWarning):
    """A submission was made, but not accepted as the machine was stopping"""
    pass


class WaitTimeout(GeneralError):
    """A .wait() timeout was hit and data was still not ready"""
    pass
