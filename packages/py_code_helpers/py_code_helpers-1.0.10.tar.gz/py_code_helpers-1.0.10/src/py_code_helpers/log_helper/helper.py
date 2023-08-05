import logging
import os

logging.basicConfig(level=logging.DEBUG)

#: lfile (str): default root log file, based on LOG_HELPER_FILE environment variable.
LFILE = os.getenv('LOG_HELPER.FILE', '/dev/null')

# root logger
fh = logging.FileHandler(LFILE)
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

def log(log_name=None, log_file=None):
    """Decorator/Wrapper for injecting the logger object as a parameter
    of the decorated method.

    Args:
       log_name (str):  Logger name. Being LOG_HELPER_NAME.log_name the result.

       log_file (str):  Logger file for writing logs to.

    Returns:
       object.  The decorated function

    Raises:
       Custom Exception

    Usage:
    ::
        import py_code_helpers.log_helper.helper as helper

        class TheClass:
            @helper.log(log_name='TestClass', log_file='/dev/null')
            def __init__(self, log):
                self.logger = log

            # and use it like:
            self.logger.info('testing log')
    """
    def decorate(function):
        def wrapper(*args, **kwargs):
            logger = logging.getLogger(log_name)
            logger.addHandler(ch)
            if log_file:
                nfh = logging.FileHandler(log_file)
                nfh.setFormatter(formatter)
                logger.addHandler(nfh)
            else:
                looger.addHandler(fh)
            function(log=logger, *args, **kwargs)
        return wrapper
    return decorate
