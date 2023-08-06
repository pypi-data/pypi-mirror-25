# Custom Exception class follows
class Error(Exception):
    """ Base class for other exceptions """
    pass


class ImProperTypeError(Error):
    """ Raised when value of DJANGO_ERROR_ASSIST_FROM variable is not of proper type.
    The expected type is str() """


class ImProperValueError(Error):
    """ Raised when value of DJANGO_ERROR_ASSIST_FROM variable is not 'google' or
    'stackoverflow' """
