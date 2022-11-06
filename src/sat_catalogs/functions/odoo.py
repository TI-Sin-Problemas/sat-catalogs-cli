"""Odoo scripts generator functions"""
from typing import Callable

from sat_catalogs.orm import SatModel, get_record_scalars

from .scripts import get_csv


def get_odoo_function(model: SatModel) -> Callable:
    """Returns the function to call to get the CSV for a model

    Args:
        model (SatModel): Model of the SQL script

    Raises:
        AttributeError: Invalid model

    Returns:
        Callable: Function to call
    """
    match model.name:
        case SatModel.TAX_SYSTEM.name:
            return get_tax_systems_csv

        case _:
            raise AttributeError("Invalid model")


def get_tax_systems_csv(db_path: str, templates_path: str) -> str:
    """Returns the tax system CSV as string

    Args:
        db_path (str): Path to the SQLite database file
        templates_path (str): Path to the template directory

    Returns:
        str: CSV string
    """
    records = get_record_scalars(SatModel.TAX_SYSTEM, db_path)

    values = []
    for rowid, record in enumerate(records, 1):
        values.append(f'tax_system_{rowid:02d},{record.id},"{record.texto}"')

    return get_csv(f"{templates_path}/odoo/tax_systems.csv", values)
