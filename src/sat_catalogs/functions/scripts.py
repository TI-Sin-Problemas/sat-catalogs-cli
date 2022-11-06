"""SQL fcripts generator functions"""


def get_sql(template_path: str, values: list) -> str:
    """Returns a SQL script formatted string replacing values from template

    Args:
        template_path (str): Path to the template file
        values (list): List of values to form the script

    Returns:
        str: SQL script formatted string
    """
    with open(f"{template_path}", "r", encoding="utf-8") as file:
        template = file.read()
    return template.replace("__values__", ",\n".join(values) + ";")


def get_csv(template_path: str, values: list) -> str:
    """Returns a csv formatted string replacing values from template

    Args:
        template_path (str): Path to the template file
        values (list): List of values to form the string

    Returns:
        str: CSV Formatted string
    """
    with open(f"{template_path}", "r", encoding="utf-8") as file:
        template = file.read()
    return template.replace("__values__", "\n".join(values))
