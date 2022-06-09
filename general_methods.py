
"""
General purpose methods that can work independently of ``bidspathlib``.

"""

import inspect
import os
import re
from os import PathLike
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


def is_hidden(src: Union[Text, os.PathLike]) -> bool:
    """
    Returns True if the name of path ``src`` starts by a dot.

    Args:
        src: Text or os.PathLike
            The path to evaluate.

    Returns: bool
    """

    return os.path.basename(src).startswith('.')


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


def flatten(nested: Iterable) -> list:
    """
    Return vectorized (1D) list from nested Sequence ``nested``.

    Args:
        nested: Sequence
           Iterable sequence containing multiple other nested sequences.

    Returns: list
        Vectorized (unidimensional) version of ``nested``.

    References: https://stackoverflow.com/questions/2158395/flatten-an-irregular-list-of-lists
    """

    yield from (flatten(x)
                if all((isinstance(x, Iterable),
                        not isinstance(x, (str, bytes))))
                else x
                for x in nested)
    # return [lowest for sublist in nested for lowest
    #         in (flatten(sublist)
    #             if bool(isinstance(sublist, Sequence)
    #                     and not isinstance(sublist, str))
    #             else [sublist])]


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


def root_path() -> Text:
    """
    Returns platform-independant root/drive directory.

    From the author:
    "On Linux this returns '/'.
    On Windows this returns 'C:\\' or whatever the current drive."

    References:
        <https://stackoverflow.com/questions/12041525/a-system-independent-way-using-python-to-get-the-root-directory-drive-on-which-p>
    """
    try:
        return os.path.abspath(os.path.sep)
    except RecursionError:
        return str(Path.cwd().root)


def _add_root(src: Union[Text, PathLike]) -> Union[Text, PathLike]:
    """
    Appends root directory or drive letter before path ``src``.

    """
    return os.path.join(root_path(), str(src))


__methods__: Tuple = (
    docstring_parameter, is_hidden, flatten, get_default_args,
    camel_to_snake, Snake2Camel, SetFromDict,
    _add_root, root_path,
    SubclassesRecursive, rev_dict
)

__all__: List = [
    "docstring_parameter", "is_hidden", "flatten",
    "get_default_args", "camel_to_snake", "Snake2Camel",
    "SetFromDict", "SubclassesRecursive", "rev_dict",
    '_add_root', 'root_path',
    "__methods__"
]
