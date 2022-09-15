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
    records = get_record_scalars("UnitOfMeasure", db_path)

    values = []
    for rowid, unit in enumerate(records, 1):
        name = unit.texto.replace("'", '"')
        description = unit.descripcion.replace("'", '"')
        values.append(f"    ({rowid}, '{unit.id}', '{name}', '{description}', 0)")

    with open(f"{templates_path}/units_of_measure.sql", "r", encoding="utf-8") as file:
        template = file.read()

    return template.replace("__values__", ",\n".join(values) + ";")
