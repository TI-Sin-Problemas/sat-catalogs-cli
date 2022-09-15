"""Main entry point"""
import os
import sqlite3
from shutil import rmtree
from tempfile import NamedTemporaryFile
from zipfile import ZipFile

import click
from requests import get

from .functions import dolibarr as dolibarr_functions


@click.group()
@click.pass_context
def cli(context: click.Context):
    """Simple CLI tool to manage SAT's catalog SQL scripts"""
    templates_path = os.path.dirname(__file__)
    context.obj = {
        "templates_path": templates_path + "/templates",
    }


@cli.group()
def dolibarr():
    """Manages Dolibar SQL scripts"""


@dolibarr.command()
@click.argument(
    "database", type=click.Path(exists=True, readable=True, resolve_path=True)
)
@click.option(
    "-m",
    "--model",
    "model",
    required=True,
    type=click.Choice(["payment_form", "unit_of_measure"], case_sensitive=False),
    help="Database object model to export",
)
@click.option(
    "-o",
    "--output",
    "output",
    type=click.Path(dir_okay=False, writable=True, resolve_path=True),
    help="Output file",
)
@click.pass_context
def export(context: click.Context, database: str, model: str, output: str):
    """Exports SQL script for Dolibarr modules

    DATABASE: SQLite database file.
    """
    model_switch = {
        "payment_form": dolibarr_functions.get_payment_forms_sql,
        "unit_of_measure": dolibarr_functions.get_units_of_measure_sql,
    }
    function = model_switch[model.lower()]
    sql = function(database, context.obj["templates_path"])

    if output:
        with open(output, "w", encoding="utf-8") as file:
            file.write(sql)
    else:
        click.echo(f"response: {sql}")


@cli.command()
def download_database():
    """Download latest SAT's catalogs database"""

    click.echo("Downloading repository...")
    request = get(
        "https://github.com/phpcfdi/resources-sat-catalogs/archive/master.zip",
        timeout=60,
    )

    with NamedTemporaryFile() as temp_file:
        temp_file.write(request.content)

        with ZipFile(temp_file.name, "r") as zip_file:
            database_dir = "resources-sat-catalogs-master/database/"
            tmp_dir = "tmp/"
            members = [
                name for name in zip_file.namelist() if name.startswith(database_dir)
            ]
            click.echo("Extracting files...")
            zip_file.extractall(tmp_dir, members)

    schemas_dir = tmp_dir + database_dir + "schemas/"
    data_dir = tmp_dir + database_dir + "data/"

    click.echo("Building database...")
    connection = sqlite3.connect("catalogs.db")
    cursor = connection.cursor()

    sql_script = ""
    for file in os.listdir(schemas_dir):
        with open(schemas_dir + file, encoding="utf-8") as script:
            sql_script += script.read()

    for file in os.listdir(data_dir):
        with open(data_dir + file, encoding="utf-8") as script:
            sql_script += script.read()

    cursor.executescript(sql_script)
    connection.close()
    click.echo("Removing temporary files...")
    rmtree(tmp_dir)
    click.echo("Done!")
