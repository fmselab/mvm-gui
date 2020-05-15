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

    extra arguments:
    - tries: the number of times to try the function before going into a permanent error state
    """

    def _wrap(self, func, *args, tries=10, **kwargs):
        """
        Wrapper function. This implements the try-catch statement

        arguments:
        - func:          the function to execute
        *args, **kwargs: positional and named arguments to pass to the
                         wrapped function
        """

        # Try the function a number of times before failing (unless had failed before)
        while tries > 0:
            tries -= 1
            try:
                return func(*args, **kwargs)
            except self.ExceptionType as error:
                self._last_error_str = str(error)
                print("ERROR in %s (%d tries left)" % (func.__name__, tries)) 
                # Run exception function (e.g. retry connect), but pass known exceptions
                if self.except_func is not None:
                    try:
                        self.except_func()
                    except self.ExceptionType:
                        pass
                print(self._last_error_str)

                
        if self.failed_func is not None:
            self.failed_func(self._last_error_str)

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
        self.failed_func = None
        self.except_func = None
        self.ExceptionType = ExceptionType
        self._last_error_str = None

        for __method in methods:
            if callable(getattr(instance, __method)) and __method[0] != '_':
                replacement = lambda *args, __method=__method, **kwargs: self._wrap(
                    getattr(instance, __method), *args, **kwargs)
                setattr(self, __method, replacement)

    def assign_failed_func(self, failed_func):
        """
        Assign an failure function to this wrapper, which will be called
        when the _wrap function has failed after certain number of tries.

        arguments:
        - failed_func:   function to call once after all retries have failed 
        """
        self.failed_func = failed_func

    def assign_except_func(self, except_func):
        """
        Assign an exception function to this wrapper, which will be called
        when an exception is raised by the _wrap function.

        arguments:
        - except_func:   function to call in the 'except' block in the
                         wrapper function.
        """
        self.except_func = except_func
