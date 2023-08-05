class ATPException(Exception):
    pass


class RetryException(ATPException):
    pass


class MaxRetriesExceed(ATPException):
    pass


__all__ = ['ATPException', 'RetryException', 'MaxRetriesExceed']
