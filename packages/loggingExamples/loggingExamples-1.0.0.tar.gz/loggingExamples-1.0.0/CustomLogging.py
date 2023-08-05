import logging


class CustomLogging:

    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

    def __init__(self, loglevel='INFO'):
        self.logger = logging.getLogger(__name__)
        if loglevel == 'CRITICAL':
            level = 50
        elif loglevel == 'ERROR':
            level = 40
        elif loglevel == 'WARNING':
            level = 30
        elif loglevel == 'INFO':
            level = 20
        elif loglevel == 'DEBUG':
            level = 10
        else:
            level = 0
        self.logger.setLevel(level)
        pass

    def custom_log_debug_message(self):
        self.logger.debug('I am DEBUG message....Logged from CustomLogging')

    def custom_log_info_message(self):
        self.logger.info('I am INFO message....Logged from CustomLogging')

    def custom_log_warn_message(self):
        self.logger.warn('I am WARN message....Logged from CustomLogging')

    def custom_log_error_message(self):
        self.logger.error('I am ERROR message....Logged from CustomLogging')

    def custom_log_critical_message(self):
        self.logger.critical('I am CRITICAL message....Logged from CustomLogging')
