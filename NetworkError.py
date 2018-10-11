import requests
import time
import logging

class NetworkError(RuntimeError):
    pass

def retryer(max_retries=10, timeout=10):
    def wraps(func):
        request_exceptions = (
            requests.exceptions.Timeout,
            requests.exceptions.ConnectionError,
            requests.exceptions.HTTPError,
            UnicodeDecodeError,
            IOError
        )

        def inner(*args, **kwargs):
            for i in range(max_retries):
                try:
                    result = func(*args, **kwargs)
                except request_exceptions:
                    time.sleep(timeout*i)
                    logging.debug("A problem occured during downloading: {} \n \
                    This is try number: {}, wait {} seconds for retry".format(NetworkError, i, timeout*i))
                    continue
                else:
                    return result
            else:
                raise NetworkError
        return inner
    return wraps
