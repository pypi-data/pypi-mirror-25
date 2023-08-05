import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create a file handler
handler = logging.FileHandler('tests_run_queue\handler_logs.log')
handler.setLevel(logging.INFO)
# add the handlers to the logger
logger.addHandler(handler)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

class Handler:

    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

    def __init__(self):
        pass

    def handler_log_debug_message(self):
        logger.debug('I am DEBUG message....Logged from Handler')

    def handler_log_info_message(self):
        logger.info('I am INFO message....Logged from Handler')

    def handler_log_warn_message(self):
        logger.warn('I am WARN message....Logged from Handler')

    def handler_log_error_message(self):
        logger.error('I am ERROR message....Logged from Handler')

    def handler_log_critical_message(self):
        logger.critical('I am CRITICAL message....Logged from Handler')
