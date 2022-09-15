"""File management functions"""

from os import listdir
from typing import Iterable, Union


def cat_files(paths: Union[Iterable[str], str], encoding: str = "utf-8") -> str:
    """Concatenates contents from a list of files or a directory

    Args:
        paths (List[str]): List of paths to files or path to a directory containing all the files
        encoding (str, optional): Name of the encoding used to decode the files. Defaults to "utf-8".

    Returns:
        str: Concatenated content from all files
    """
    result = ""

    if isinstance(paths, str):
        paths = [f"{paths}{filename}" for filename in listdir(paths)]

    for path in paths:
        with open(path, encoding=encoding) as file:
            result += file.read()
    return result
