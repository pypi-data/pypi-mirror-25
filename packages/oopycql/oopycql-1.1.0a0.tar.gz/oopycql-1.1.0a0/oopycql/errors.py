

class ParameterNotSetError(KeyError):
    """Raised by ParameterMap when an attempt is made to set the value
    of a parameter which is not specified in the query."""
    pass
