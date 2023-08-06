"""Python library for assisting with the deprecation process."""
__version__ = "0.1.0"

__url__ = "https://github.com/AndyDeany/deprecationlib"
__download_url__ = "{}/archive/{}.tar.gz".format(__url__, __version__)
__author__ = "Andrew Dean"
__author_email__ = "oneandydean@hotmail.com"


from functools import wraps
import warnings


warnings.simplefilter("always", DeprecationWarning)

def deprecated(alternative="an alternative"):
    """Decorator for marking a function or method as deprecated."""
    def warn(function, alternative):
        details = (function.__name__, alternative)
        message = "{}() is deprecated. Please use {} instead.".format(*details)
        warnings.warn(message, DeprecationWarning)

    if callable(alternative):
        @wraps(alternative)
        def deprecated_function(*args, **kwargs):
            warn(alternative, "an alternative")
            return alternative(*args, **kwargs)
        return deprecated_function

    def decorator(function):
        @wraps(function)
        def deprecated_function(*args, **kwargs):
            warn(function, alternative)
            return function(*args, **kwargs)
        return deprecated_function
    return decorator
