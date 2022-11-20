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
    function_map = {
        SatModel.FORM_OF_PAYMENT.name: get_payment_forms_csv,
        SatModel.TAX_SYSTEM.name: get_tax_systems_csv,
        SatModel.PROD_SERV_KEY.name: get_product_service_keys_csv,
        SatModel.UNIT_OF_MEASURE.name: get_units_of_measure_csv,
        SatModel.CFDI_USE.name: get_cfdi_uses_csv,
    }

    try:
        return function_map[model.name]
    except KeyError as err:
        raise AttributeError("Invalid model") from err


def get_units_of_measure_csv(db_path: str, templates_path: str) -> str:
    """Returns the units of measurement CSV as string

    Args:
        db_path (str): Path to the SQLite database file
        templates_path (str): Path to the template directory

    Returns:
        str: CSV string
    """
    records = get_record_scalars(SatModel.UNIT_OF_MEASURE, db_path)

    values = []
    for rowid, record in enumerate(records, 1):
        values.append(f'unit_of_measure_{rowid:04d},{record.id},"{record.texto}"')

    return get_csv(f"{templates_path}/odoo/units_of_measure.csv", values)


def get_payment_forms_csv(db_path: str, templates_path: str) -> str:
    """Returns the payment forms CSV as string

    Args:
        db_path (str): Path to the SQLite database file
        templates_path (str): Path tho the template directory

    Returns:
        str: CSV string
    """
    records = get_record_scalars(SatModel.FORM_OF_PAYMENT, db_path)

    values = []
    for rowid, record in enumerate(records, 1):
        values.append(f'payment_form_{rowid:02d},{record.id},"{record.texto}"')

    return get_csv(f"{templates_path}/odoo/payment_forms.csv", values)


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


def get_product_service_keys_csv(db_path: str, templates_path: str) -> str:
    """Returns the product/service keys CSV as string

    Args:
        db_path (str): Path to the SQLite database file
        templates_path (str): Path to the template directory

    Returns:
        str: CSV string
    """

    records = get_record_scalars(SatModel.PROD_SERV_KEY, db_path)

    values = []
    for rowid, record in enumerate(records, 1):
        values.append(f'prod_serv_key_{rowid:05d},{record.id},"{record.texto}"')
    return get_csv(f"{templates_path}/odoo/product_service_keys.csv", values)


def get_cfdi_uses_csv(db_path: str, templates_path: str) -> str:
    """Returns the CFDI use CSV as string

    Args:
        db_path (str): Path to the SQLite database
        templates_path (str): Path to the template directory

    Returns:
        str: CSV string
    """
    records = get_record_scalars(SatModel.CFDI_USE, db_path)

    values = []
    for rowid, record in enumerate(records, 1):
        values.append(f'cfdi_use_{rowid:02d},{record.id},"{record.texto}"')
    return get_csv(f"{templates_path}/odoo/cfdi_uses.csv", values)
