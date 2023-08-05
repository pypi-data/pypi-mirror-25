from robot.api import logger


class RobotLog:

    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

    def __init__(self):
        pass

    def robot_log_debug_message(self):
        logger.debug('I am DEBUG message....Logged from RobotLog')

    def robot_log_info_message(self):
        logger.info('I am INFO message....Logged from RobotLog')

    def robot_log_warn_message(self):
        logger.warn('I am WARN message....Logged from RobotLog')

    def robot_log_error_message(self):
        logger.error('I am ERROR message....Logged from RobotLog')

    def robot_log_critical_message(self):
        logger.critical('I am CRITICAL message....Logged from RobotLog')
