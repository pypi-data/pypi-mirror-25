import logging


# Decorator to handle events
def my_decorator(func):
    def decorator(self):
        try:
            func(self)
            self.logger.info('Hurray........ No Error From me.... I am Clean')
        except ZeroDivisionError, e:
            self.logger.error('Decorator handled exception %s' % e)
            self.logger.warn('Hey.....Remove error by avoiding division by zero')
            #raise
        except TypeError, e:
            self.logger.error('Decorator handled exception %s' % e)
            self.logger.warn('Hey.....Can you check for type of arguments used?')
            #raise
    return decorator


class DecoratorLogging:

    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    @my_decorator
    def decorator_division_by_zero(self):
        self.logger.info('Logged from DecoratorLogging... Performing Division by Zero')
        x = 1 / 0

    @my_decorator
    def decorator_type_error(self):
        self.logger.info('Logged from DecoratorLogging... Performing Type Error')
        x = 1 + 'abc'

    @my_decorator
    def decorator_no_error(self):
        self.logger.info('Logged from DecoratorLogging... Performing No Error')
        x = 1 + 2
