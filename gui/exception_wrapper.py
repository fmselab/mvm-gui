"""
ExceptionWrapper

This module implements the concept of a exception wrapper, i.e. a
technique to wrap all public methods of a given class inside a try-except
statement that, in case one of the given exceptions is raised, executes a
defined function.

All public members are automatically wrapped regardless what their
signatures or names are.
"""


class ExceptionWrapper:
    #pylint: disable=too-few-public-methods
    """
    The ExceptionWrapper class.

    It has only the constructor, but it will automagically generate all
    other methods starting from the public methods of the provided class.
    """

    def _wrap(self, func, *args, **kwargs):
        """
        Wrapper function. This implements the try-catch statement

        arguments:
        - func:          the function to execute
        *args, **kwargs: positional and named arguments to pass to the
                         wrapped function
        """

        try:
            return func(*args, **kwargs)
        except self.ExceptionType:
            self.except_func()

    def __init__(self, instance, ExceptionType, except_func):
        #pylint: disable=invalid-name
        """
        Constructor.

        It implements public methods by wrapping that of 'instance' within
        the _wrap function.

        arguments:
        - instance:      an instance of an arbitrary object to wrap public
                         methods
        - ExceptionType: the Exception class or tuple of Exception classes
                         to catch in the wrapper.
        - except_func:   function to call in the 'except' block in the
                         wrapper function.
        """

        methods = dir(instance)
        self.except_func = except_func
        self.ExceptionType = ExceptionType
        for __method in methods:
            if callable(getattr(instance, __method)) and __method[0] != '_':
                replacement = lambda *args, __method=__method, **kwargs: self._wrap(
                    getattr(instance, __method), *args, **kwargs)
                setattr(self, __method, replacement)
