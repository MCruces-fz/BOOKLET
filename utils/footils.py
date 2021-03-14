import os
from typing import Union
from decimal import Decimal


# TODO:
#  - Choose language
#  - Choose theme (dark / light)
#  - Choose if write signature at the end.
#  - Make a config file.json with all settings like in:
#    https://es.stackoverflow.com/questions/198057/cambiar-color-de-pesta%C3%B1a-seleccionada-en-ttk-notebook

def inch2mm(value: Union[int, float, Decimal]) -> float:
    """
    Conversion of inches to millimeters.

    :param value: Value in inches to convert to millimeters.
    :return: Value in millimeters.
    """
    return round(float(value) * 25.4 / 72, 3)


def mm2inch(value: Union[int, float, Decimal]) -> float:
    """
    Conversion of millimeters to inches.

    :param value: Value in millimeters to convert to inches.
    :return: Value in inches.
    """
    return round(float(value) * 72 / 25.4, 3)


def basename(full_path: str, extension: bool = False) -> str:
    """
    Get the file name from a path.

    :param full_path: Full path to the file.
    :param extension: True if return name with extensions (False by default)
    :return: The name ID of the file (without extension by default)
    """
    filename = os.path.basename(full_path)
    if not extension:
        filename = os.path.splitext(filename)[0]
    return filename
