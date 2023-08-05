import logging


class LibraryListenerLogging:
    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self):
        self.ROBOT_LIBRARY_LISTENER = self
        self.logger = logging.getLogger(__name__)

    def _start_suite(self, name, attrs):
        self.logger.info('Suite %s (%s) starting.' % (name, attrs['id']))
        self.logger.info('Hey.... I am Library Listener at START of SUITE... Probably I can do something for you!!!')

    def _start_test(self, name, attrs):
        self.logger.info('Test %s (%s) starting.' % (name, attrs['id']))
        self.logger.info('Hey.... I am Library Listener at START of TEST... Probably I can do something for you!!!')

    def _end_test(self, name, attrs):
        self.logger.info('Test %s (%s) ending.' % (name, attrs['id']))
        self.logger.info('Hey.... I am Library Listener at END of TEST... Probably I can do something for you!!!')

    def _end_suite(self, name, attrs):
        self.logger.info('Suite %s (%s) ending.' % (name, attrs['id']))
        self.logger.info('Hey.... I am Library Listener at END of SUITE... Probably I can do something for you!!!')

    def log_debug_message(self):
        self.logger.debug('I am DEBUG message....Logged from LibraryListenerLogging')

    def log_info_message(self):
        self.logger.info('I am INFO message....Logged from LibraryListenerLogging')

    def log_warn_message(self):
        self.logger.warn('I am WARN message....Logged from LibraryListenerLogging')

    def log_error_message(self):
        self.logger.error('I am ERROR message....Logged from LibraryListenerLogging')

    def log_critical_message(self):
        self.logger.critical('I am CRITICAL message....Logged from LibraryListenerLogging')
