import io, typing

_T = typing.TypeVar('_T')
def ExtraType(name: str, tp: typing.Type[_T], factory) -> typing.Type[_T]:
    """
    Extends the functionality of typing.NewType to attach the validation function
    :param name: See typing.NewType(name)
    :param tp:   See typing.NewType(name)
    :param factory: The factory function called to instantiate the value of the variable, must have same signature as tp.__new__()
    :return: See typing.NewType
    """
    x = typing.NewType(name, tp)
    x.__new__ = factory
    return x

def PathOrStream(mode):
    def PathOrStream_Factory(cls, val, *args, **kwargs) -> io.IOBase:
        if isinstance(val, io.IOBase):
            return val
    return ExtraType('PathOrStream_{}'.format(mode), io.IOBase, PathOrStream_Factory)