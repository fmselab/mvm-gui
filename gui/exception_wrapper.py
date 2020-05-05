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

        print("We are wrapping")

        try:
            print("Trying to run ", func)
            if self.except_state: raise self.ExceptionType()
            self._last_func = lambda func=func: self._wrap(func, *args, **kwargs)
            return func(*args, **kwargs)
        except self.ExceptionType:
            self.exception_state = True
            if self.except_func is not None:
                print("Caught the exception")
                self.except_func()
                print('Done catching exception')
            raise

    def __init__(self, instance, ExceptionType):
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
        """

        methods = dir(instance)
        self.except_func = None
        self.except_state = False
        self.ExceptionType = ExceptionType
        self._last_func_call = None

        for __method in methods:
            if callable(getattr(instance, __method)) and __method[0] != '_':
                replacement = lambda *args, __method=__method, **kwargs: self._wrap(
                    getattr(instance, __method), *args, **kwargs)
                setattr(self, __method, replacement)
    
    def assign_except_func(self, except_func):
        """
        Assign an exception function to this wrapper, which will be called
        when an exception is raised by the _wrap function.

        arguments:
        - except_func:   function to call in the 'except' block in the
                         wrapper function.
        """
        self.except_func = except_func
