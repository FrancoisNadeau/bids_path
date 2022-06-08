
class ErrorCheck:
    """
    Python decorator to check error parameter.

    Implementation:

        @ErrorCheck
        def add_numbers(*numbers):
            return sum(numbers)
    """

    def __init__(self, function):
        self.function = function

    def __call__(self, *params):
        if any([isinstance(i, str) for i in params]):
            raise TypeError("parameter cannot be a string !!")
        else:
            return self.function(*params)
