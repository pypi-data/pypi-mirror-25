""" This module contains the exceptions for the football-data.org api wrapper """

class IncorrectMethodCallException(Exception):
    '''Raise when the parameters of a method call are incorrect'''
    def __init__(self, message, *args):
        self.message = message
        super(IncorrectMethodCallException, self).__init__(message, *args)

class IncorrectParametersException(Exception):
    '''Raise when the parameters of a request are incorrect'''
    def __init__(self, message, main, main_id, sub, filters, *args):
        self.message = message
        self.main = main
        self.main_id = main_id
        self.sub = sub
        self.filters = filters
        super(IncorrectParametersException, self).__init__(message, main, main_id, sub, filters, *args)

class IncorrectFilterException(Exception):
    '''Raise when the parameters of a filter are incorrect'''
    def __init__(self, message, resource, filtername, filtervalue, *args):
        self.message = message
        self.resource = resource
        self.filtername = filtername
        self.filtervalue = filtervalue
        super(IncorrectFilterException, self).__init__(message, resource, filtername, filtervalue, *args)

class APIErrorException(Exception):
    '''Raise when a request returns with an error'''
    def __init__(self, message, status_code, *args):
        self.message = message
        self.status_code = status_code
        super(APIErrorException, self).__init__(message, status_code, *args)
