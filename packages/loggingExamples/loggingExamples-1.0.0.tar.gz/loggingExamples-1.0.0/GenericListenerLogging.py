import logging


class GenericListenerLogging:

    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.ROBOT_LIBRARY_LISTENER = self

    def start_suite(self, name, attrs):
        self.logger.info('Suite %s (%s) starting.' % (name, attrs['id']))
        self.logger.info('Hey.... I am Generic Listener at START of SUITE... Probably I can do something for you!!!')

    def start_test(self, name, attrs):
        self.logger.info('Test %s (%s) starting.' % (name, attrs['id']))
        self.logger.info('Hey.... I am Generic Listener at START of TEST... Probably I can do something for you!!!')

    def end_test(self, name, attrs):
        self.logger.info('Test %s (%s) ending.' % (name, attrs['id']))
        self.logger.info('Hey.... I am Generic Listener at END of TEST... Probably I can do something for you!!!')

    def end_suite(self, name, attrs):
        self.logger.info('Suite %s (%s) ending.' % (name, attrs['id']))
        self.logger.info('Hey.... I am Generic Listener at END of SUITE... Probably I can do something for you!!!')