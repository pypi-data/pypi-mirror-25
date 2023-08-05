import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class DemoLogging:

    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

    def __init__(self):
        pass

    def log_debug_message(self):
        logger.debug('I am DEBUG message....Logged from DemoLogging')

    def log_info_message(self):
        logger.info('I am INFO message....Logged from DemoLogging')

    def log_warn_message(self):
        logger.warn('I am WARN message....Logged from DemoLogging')

    def log_error_message(self):
        logger.error('I am ERROR message....Logged from DemoLogging')

    def log_critical_message(self):
        logger.critical('I am CRITICAL message....Logged from DemoLogging')
