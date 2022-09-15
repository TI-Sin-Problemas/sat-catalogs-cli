"""Dolibarr scripts generator functions"""
from sat_catalogs.orm import get_record_scalars


def get_units_of_measure_sql(db_path: str, templates_path: str) -> str:
    """Returns the unit of measure SQL script as string

    Args:
        db_path (str): Path to the SQLite database file
        templates_path (str): Path to the scripts template directory

    Returns:
        str: SQL script
    """
    records = get_record_scalars("unit_of_measure", db_path)

    values = []
    for rowid, record in enumerate(records, 1):
        name = record.texto.replace("'", '"')
        description = record.descripcion.replace("'", '"')
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
    records = get_record_scalars("payment_form", db_path)

    values = []
    for rowid, record in enumerate(records, 1):
        name = record.texto.replace("'", '"')
        values.append(f"    ({rowid}, '{record.id}', '{name}', 0)")

    with open(f"{templates_path}/payment_forms.sql", "r", encoding="utf-8") as file:
        template = file.read()

    return template.replace("__values__", ",\n".join(values) + ";")
