
"""
General purpose methods that can work independently of ``bidspathlib``.

"""

import hashlib
import inspect
import os
import re
from gzip import decompress
from io import BytesIO
from pathlib import Path
from typing import (
    Any, Dict, Iterable, List, NoReturn,
    Optional, Text, Tuple, Union
)

__path__ = [os.path.join('..', '__init__.py')]


def docstring_parameter(*sub: Union[Text, Iterable]):
    """
    Allows insertion of string variables in documentation.

    Args:
        *sub: str
            The variable(s) to insert

    Returns: Function (python decorator)

    References:
        <https://stackoverflow.com/questions/10307696/how-to-put-a-variable-into-python-docstring>
    """

    def dec(obj):
        obj.__doc__ = obj.__doc__.format(*sub)
        return obj
    return dec


def get_default_args(func: callable) -> Dict:
    """
    Return a dict containing the default arguments of ``func``.

    Useful for allowing keyword arguments being passed to another function.

    Args:
        func: callable
            A callable function from which to retrieve its default parameters.

    Returns: dict
        Dictionary containing a function's default parameters.

    References:
        <https://stackoverflow.com/questions/12627118/get-a-function-arguments-default-value>
    """
    signature = inspect.signature(func)
    return {k: v.default for k, v in signature.parameters.items()
            if v.default is not inspect.Parameter.empty}


def camel_to_snake(name: Text) -> Text:
    """
    Converts a CamelCaseString to snake_case_string.

    Args:
        name: str
            The text to convert.

    Returns: str
        The converted CamelCaseString to snake_case_string.

    References:
        <https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case>
    """
    pat0 = re.compile('(.)([A-Z][a-z]+)')
    pat1 = re.compile('([a-z\d])([A-Z])')
    name = pat0.sub(r'\1_\2', name)
    return pat1.sub(r'\1_\2', name).lower()


def Snake2Camel(name: Text) -> Text:
    """
    Converts a snake_case_string to CamelCaseString.

    Args:
        name: str
            The text to convert.

    Returns: str
        The converted snake_case_string to CamelCaseString.
    """
    from string import capwords
    return capwords(name.replace("_", " ")).replace(" ", "")


def SetFromDict(obj: Any,
                attrs: Dict,
                keys: Optional[Iterable] = None,
                default: Optional[Text] = '',
                **kwargs) -> NoReturn:
    """
    Sets class attributes defined in ``__slots__`` inplace.

    Args:
        obj: object
            The class instance.

        attrs: Dict
            Dictionary mapping the attributes defines in
            ``cls.__slots__`` to their values.

        keys: Iterable (Default = None)
            Subset of keys in ``attrs`` to use.

        default: str (Default = '')
            Optional default value substitution.

        kwargs: Dict
            Dictionary allowing to change default parameters.

    Returns: None
    """

    kwargs = kwargs if kwargs is not None else {}
    attrs = attrs if attrs is not None else {}
    attrs = {**attrs, **kwargs}
    keys = keys if keys is not None else tuple(attrs.keys())
    [setattr(obj, key, attrs.get(key, default))
     for key in keys]


def SubclassesRecursive(cls: Any, as_dict: bool = True
                        ) -> Union[Dict, List]:
    """
    Returns a list or a dict of all classes subclassed by ``cls``.

    Args:
        cls: Any
            Python object having subclasses.

        as_dict: bool (Default=True)
            If True, returns a ``dict`` containing the
            subclasses of object ``cls``.
            Otherwise, return a list of subclasses.

    Returns:
        Union[List, Dict]:

    Example:
        >>> SubclassesRecursive(cls, as_dict=True)
            {_cls.__name__: _cls}

    References:
        <https://blog.finxter.com/how-to-find-all-the-subclasses-of-a-class/>
    """
    direct = cls.__subclasses__()
    indirect = []
    for subclass in direct:
        indirect.extend(cls.subclasses_recursive(subclass))
    subclasses = direct + indirect
    return {_cls.__name__: _cls
            for _cls in direct + indirect} \
        if as_dict else subclasses


def rev_dict(dc: Dict) -> Dict:
    """
    Return dict inversely mapping key-value pairs in ``dc``.

    """
    return dict(tuple((i[1], i[0]) for i in tuple(dc.items())))


def even_seq(it: Iterable) -> Tuple:
    """
    Returns elements indexed at even positions in an iterable.

    Args:
        it: Iterable

    Returns: Tuple

    """
    return tuple(i[1] for i in enumerate(it) if i[0] % 2 == 0)


def odd_seq(it: Iterable) -> Tuple:
    """
    Returns elements indexed at odd positions in an iterable.

    Args:
        it: Iterable

    Returns: Tuple

    """
    return tuple(i[1] for i in enumerate(it) if i[0] % 2 != 0)


def get_desc(function_name: str) -> tuple:
    """
    Parse a function's docstring automatically

    Useful to provide ``argparse.ArgumentParser`` object both
    ``usage`` and ``description`` parameters with
    each argument's help message.

    Args:
        function_name: str
            Name of the function for which to get documentation from.

    Returns: tuple(desc, help_msgs)
        desc: str
            Concatenation of short and long function descriptions
        help_msgs: tuple(str)
            Tuple of strings representing each parameter's help message
    """

    from docstring_parser import parse as ds_parse

    parsed = ds_parse(function_name.__doc__)
    help_msgs = tuple(prm.description for prm
                      in parsed.params)
    desc = '\n'.join([parsed.short_description,
                      parsed.long_description])
    return desc, help_msgs


def sizeof_fmt(num: int) -> Text:
    """
    Returns the size of the input formatted to be human-readable.

    Args:
        num: int
            Integer representing the number of bytes to format.

    Returns: str
        String representing the formatted input size.

    References:
        https://stackoverflow.com/questions/1094841/get-human-readable-version-of-file-size
    """

    for unit in ('', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi'):
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, 'B')
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', 'B')


def GetMD5CheckSum(src: Union[Text, os.PathLike],
                   unzip: bool = False) -> Text:
    """
    Returns the MD5 checksum of a file as a hexadecimal string.

    Args:
        src: Text or PathLike
            Path of a file.

        unzip: bool (Default=False)
            Indicates if the bytes stream should be decompressed
            using ``gzip`` or not.

    Returns: Text
        String of double length, containing only hexadecimal digits.
    """
    m, _src = hashlib.md5(), Path(src).read_bytes
    _stream = BytesIO(decompress(_src())) \
        if unzip else BytesIO(_src())
    [m.update(line) for line in _stream.readlines()]
    return m.hexdigest()


def GetSha1Sum(src: Union[Text, os.PathLike],
               unzip: bool = False) -> Text:
    """
    Returns the sha1 checksum of file ``src`` as a hexadecimal string.

    Args:
        src: str or PathLike
            The path of the file to verify.

        unzip: bool (Default=False)
            If the file should be decompressed
            using gzip or not.

    Returns: str
        Hexadecimal string
    """
    m, _src = hashlib.sha1(), Path(src)
    _buf = BytesIO(_src.read_bytes()) if not unzip else \
        BytesIO(decompress(_src.read_bytes()))
    [m.update(line) for line in _buf.readlines()]
    return m.hexdigest()


__methods__: Tuple = (
    docstring_parameter, get_default_args, camel_to_snake,
    Snake2Camel, SetFromDict, SubclassesRecursive,
    rev_dict, even_seq, odd_seq, get_desc, sizeof_fmt,
    GetMD5CheckSum, GetSha1Sum
)

__all__: List = [
    "docstring_parameter", "get_default_args", "camel_to_snake",
    "Snake2Camel", "SetFromDict", "SubclassesRecursive",
    "rev_dict", "even_seq", "odd_seq", "get_desc", "sizeof_fmt",
    "GetMD5CheckSum", "GetSha1Sum",
    "__methods__"
]
