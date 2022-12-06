"""ERP Next fixtures generator functions"""
from typing import Callable
from click.exceptions import BadParameter

from sat_catalogs.orm import SatModel, get_record_scalars

from . import scripts


def get_erpnext_function(model: SatModel) -> Callable:
    """Returns the function to call to get the JSON string for a model

    Args:
        model (SatModel): Model of the SQL script

    Raises:
        BadParameter: Invalid model

    Returns:
        Callable: Function to call
    """

    function_map = {
        SatModel.FORM_OF_PAYMENT.name: get_ways_to_pay,
        SatModel.TAX_SYSTEM.name: get_tax_systems,
        SatModel.PROD_SERV_KEY.name: get_product_service_keys,
        SatModel.UNIT_OF_MEASURE.name: get_uom_keys,
        SatModel.CFDI_USE.name: get_cfdi_uses,
    }

    try:
        return function_map[model.name]
    except KeyError as err:
        raise BadParameter("Invalid model") from err


def get_uom_keys(db_path: str, *args) -> str:
    """Returns the unit of measue keys JSON string

    Args:
        db_path (str): Path to the SQLite database file

    Returns:
        str: JSON string
    """
    records = get_record_scalars(SatModel.UNIT_OF_MEASURE, db_path)
    values = [
        {
            "description": record.descripcion,
            "doctype": "SAT UOM Key",
            "enabled": 1,
            "key": record.id,
            "key_name": f"{record.id} - {record.texto}",
            "name": record.id,
            "uom_name": record.texto,
        }
        for record in records
    ]

    return scripts.get_json(values)


def get_ways_to_pay(db_path: str, *args) -> str:
    """Returns the ways to pay as a JSON string

    Args:
        db_path (str): Path to the SQLite database file

    Returns:
        str: JSON string
    """
    records = get_record_scalars(SatModel.FORM_OF_PAYMENT, db_path)
    values = [
        {
            "description": record.texto,
            "doctype": "SAT Way To Pay",
            "enabled": 1,
            "key": record.id,
            "key_name": f"{record.id} - {record.texto}",
            "name": record.id,
        }
        for record in records
    ]
    return scripts.get_json(values)


def get_product_service_keys(db_path: str, *args) -> str:
    """Returns the product/service keys JSON string

    Args:
        db_path (str): Path to the SQLite database file

    Returns:
        str: JSON string
    """
    records = get_record_scalars(SatModel.PROD_SERV_KEY, db_path)
    values = [
        {
            "description": record.texto,
            "doctype": "SAT Product or Service Key",
            "enabled": 1,
            "key": record.id,
            "key_name": f"{record.id} - {record.texto}"[:140],
            "name": record.id,
        }
        for record in records
    ]

    return scripts.get_json(values)


def get_tax_systems(db_path: str, *args) -> str:
    """Returns the tax systems JSON string

    Args:
        db_path (str): Path to the SQLite database file

    Returns:
        str: JSON string
    """
    records = get_record_scalars(SatModel.TAX_SYSTEM, db_path)
    values = [
        {
            "description": record.texto,
            "doctype": "SAT Tax System",
            "enabled": 1,
            "key": record.id,
            "key_name": f"{record.id} - {record.texto}"[:140],
            "name": record.id,
        }
        for record in records
    ]

    return scripts.get_json(values)


def get_cfdi_uses(db_path: str, *args) -> str:
    """Retruns the CFDI uses JSON string

    Args:
        db_path (str): Path to the SQLite database file

    Returns:
        str: JSON string
    """
    recods = get_record_scalars(SatModel.TAX_SYSTEM, db_path)
    values = [
        {
            "description": record.texto,
            "doctype": "SAT Tax System",
            "enabled": 1,
            "key": record.id,
            "key_name": f"{record.id} - {record.texto}"[:140],
            "name": record.id,
        }
        for record in recods
    ]

    return scripts.get_json(values)
