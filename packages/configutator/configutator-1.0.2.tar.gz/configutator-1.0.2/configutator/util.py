import types, re
from inspect import getdoc

# Regular expression to use to extract parameter descriptions from function docstrings.
# It must return two capture groups, the parameter name and the doc string.
argDocRegEx = re.compile(r':param ([^:]+):[\t ]*(.+)$', flags=re.MULTILINE)

def normaliseArgs(func: types.FunctionType, args: list, kwargs: dict) -> dict:
    """
    Merges args and kwargs into a single dict.

    :param func: Function whose arguments to match against.
    :param args: Positional arguments that coincide with func's parameters.
    :param kwargs: Keyword arguments that coincide with func's parameters.
    :return: Dict indexed on funcs parameter names with the values of args and kwargs.
        kwargs will override any conflicts with args.
    """
    mergedArgs = dict(zip(func.__code__.co_varnames[:func.__code__.co_argcount], args))
    mergedArgs.update(kwargs)
    return mergedArgs


def getParamDoc(func) -> dict:
    """
    Helper to parse out parameter documentation using :data:`argDocRegEx`.

    :param func: The function to retrieve the docstring using :func:`inspect.getdoc`.
    :return: dictionary of documentation keyed on parameter name.
    """
    return {match.group(1): match.group(2) for match in argDocRegEx.finditer(getdoc(func) or "")}

def getTrueAnnotationType(annotation):
    """
    Resolve the supertype of an annotation type possibly created using the typing module.

    :param annotation: A type object.
    :return: The original object or its supertype.
    """
    return getattr(annotation, '__supertype__', annotation)

def strtobool(val: str) -> bool:
    """Convert a string representation of truth to true or false.

    True values are 'y', 'yes', 't', 'true', 'on', and '1'.
    False values are 'n', 'no', 'f', 'false', 'off', and '0'.
    Raises ValueError if 'val' is anything else.

    Taken from distutils.util and modified to return correct type.
    """
    val = val.lower()
    if val in ('y', 'yes', 't', 'true', 'on', '1'):
        return True
    elif val in ('n', 'no', 'f', 'false', 'off', '0'):
        return False
    else:
        raise ValueError("invalid truth value %r" % (val,))
