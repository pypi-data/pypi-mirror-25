import logging


class PropertyLogging:

    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.level = 0

    #@property
    def log_level(self, loglevel='INFO'):
        if loglevel == 'CRITICAL':
            self.level = 50
        elif loglevel == 'ERROR':
            self.level = 40
        elif loglevel == 'WARNING':
            self.level = 30
        elif loglevel == 'INFO':
            self.level = 20
        elif loglevel == 'DEBUG':
            self.level = 10
        else:
            self.level = 0

        self.logger.setLevel(self.level)
        pass

    def property_log_debug_message(self):
        self.logger.debug('I am DEBUG message....Logged from PropertyLogging')

    def property_log_info_message(self):
        self.logger.info('I am INFO message....Logged from PropertyLogging')

    def property_log_warn_message(self):
        self.logger.warn('I am WARN message....Logged from PropertyLogging')

    def property_log_error_message(self):
        self.logger.error('I am ERROR message....Logged from PropertyLogging')

    def property_log_critical_message(self):
        self.logger.critical('I am CRITICAL message....Logged from PropertyLogging')
