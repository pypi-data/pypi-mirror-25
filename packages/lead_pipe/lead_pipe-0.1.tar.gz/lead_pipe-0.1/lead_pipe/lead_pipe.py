class Pipe:
    """
    Represents a pipe that, when called, calls a given function with its value
    as the first argument.
    """
    def __init__(self, value):
        """
        Creates a new pipe with a given value.

        >>> Pipe(3)
        Pipe(3)
        >>> Pipe('a')
        Pipe('a')
        """
        self.value = value
    
    def __call__(self, function, *args, **kwargs):
        """
        Pipes the value of self into a given function with additional args.
        
        >>> Pipe(2)('{a} {} {b} {}'.format, 4, a=1, b=3)
        Pipe('1 2 3 4')
        """
        return Pipe(function(self.value, *args, **kwargs))
    
    def __invert__(self):
        """
        Returns the value of the pipe.
        
        >>> ~Pipe('abc')
        'abc'
        """
        return self.value
    
    def __repr__(self):
        """
        Returns a readable representation of pipe with value.

        >>> Pipe(12)
        Pipe(12)
        >>> Pipe('12')
        Pipe('12')
        """
        return ~self(repr)('Pipe({})'.format)

def apply(function, *args, **kwargs):
    """
    Calls a given function with given arguments.

    >>> apply(str, 24)
    '24'
    """
    return function(*args, **kwargs)

def reflect(value, attribute, *args, **kwargs):
    """
    Combination of getattr and apply. Used to invoke a member function within
    a pipeline.

    >>> reflect({'a': 3}, 'get', 'a')
    3
    """
    return ~Pipe(value)(getattr, attribute)(apply, *args, **kwargs)
