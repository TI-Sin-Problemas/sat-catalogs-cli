"""Dolibarr scripts generator functions"""
from typing import Callable

from sat_catalogs.orm import SatModel, get_record_scalars


def get_dolibarr_function(model: SatModel) -> Callable:
    """Returns the function to call to get the SQL script for a model

    Args:
        model (SatModel): Model of the SQL script

    Raises:
        AttributeError: Invalid model

    Returns:
        Callable: Function to call
    """
    match model.name:
        case SatModel.FORM_OF_PAYMENT.name:
            return get_payment_forms_sql

        case SatModel.UNIT_OF_MEASURE.name:
            return get_units_of_measure_sql

        case _:
            raise AttributeError("Invalid model")


def get_units_of_measure_sql(db_path: str, templates_path: str) -> str:
    """Returns the unit of measure SQL script as string

    Args:
        db_path (str): Path to the SQLite database file
        templates_path (str): Path to the scripts template directory

    Returns:
        str: SQL script
    """
    records = get_record_scalars(SatModel.UNIT_OF_MEASURE, db_path)

    values = []
    for rowid, record in enumerate(records, 1):
        name = record.texto.replace("'", '"')
        description = record.descripcion.replace("'", '"').replace(";", ",")
        values.append(f"    ({rowid}, '{record.id}', '{name}', '{description}', 0)")

    with open(f"{templates_path}/units_of_measure.sql", "r", encoding="utf-8") as file:
        template = file.read()

    return template.replace("__values__", ",\n".join(values) + ";")


def get_payment_forms_sql(db_path: str, templates_path: str) -> str:
    """Returns the payment forms SQL script as string

    Args:
        db_path (str): Path to the SQLite database file
        templates_path (str): Path to the scripts template directory

    Returns:
        str: SQL script
    """
    records = get_record_scalars(SatModel.FORM_OF_PAYMENT, db_path)

    values = []
    for rowid, record in enumerate(records, 1):
        name = record.texto.replace("'", '"')
        values.append(f"    ({rowid}, '{record.id}', '{name}', 0)")

    with open(f"{templates_path}/payment_forms.sql", "r", encoding="utf-8") as file:
        template = file.read()

    return template.replace("__values__", ",\n".join(values) + ";")
