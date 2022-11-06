"""Main entry point"""
import os
import sqlite3
from shutil import rmtree
from tempfile import NamedTemporaryFile
from zipfile import ZipFile

import click
from requests import get

from . import files
from .functions.dolibarr import get_dolibarr_function
from .functions.odoo import get_odoo_function
from .orm import SatModel


@click.group()
@click.pass_context
def cli(context: click.Context):
    """Simple CLI tool to manage SAT's catalog SQL scripts"""
    templates_path = os.path.dirname(__file__)
    context.obj = {
        "templates_path": templates_path + "/templates",
    }


@cli.command()
@click.argument(
    "database", type=click.Path(exists=True, readable=True, resolve_path=True)
)
@click.argument("system", type=click.Choice(["dolibarr", "odoo"]))
@click.option(
    "-m",
    "--model",
    "model",
    required=True,
    type=click.Choice([model.name for model in SatModel], case_sensitive=False),
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
def export(context: click.Context, database: str, system: str, model: str, output: str):
    """Exports data script for ERP modules

    DATABASE: SQLite database file.\n
    SYSTEM: ERP System where script is going to be used
    """
    functions_map = {"dolibarr": get_dolibarr_function, "odoo": get_odoo_function}
    dolibarr_function = functions_map[system](SatModel[model])
    sql = dolibarr_function(  # pylint: disable=not-callable
        database, context.obj["templates_path"]
    )

    if output:
        with open(output, "w", encoding="utf-8") as file:
            file.write(sql)
    else:
        click.echo(f"response: {sql}")


@cli.command()
@click.option(
    "-n",
    "--name",
    "db_path",
    type=click.Path(dir_okay=False, writable=True, resolve_path=True),
    default="catalogs.db",
    show_default=True,
    help="Name or path to build the database",
)
@click.option(
    "-o",
    "--overwrite",
    "overwrite",
    is_flag=True,
    default=False,
    show_default=True,
    help="Allow overwriting database file",
)
def build_database(db_path: str, overwrite: bool):
    """Download and build latest SAT's catalogs database"""

    click.echo("⇩ Downloading repository...")
    url = "https://github.com/phpcfdi/resources-sat-catalogs/archive/master.zip"
    request = get(url, timeout=60)

    with NamedTemporaryFile() as temp_file:
        temp_file.write(request.content)

        with ZipFile(temp_file.name, "r") as zip_file:
            database_dir = "resources-sat-catalogs-master/database/"
            tmp_dir = "tmp/"
            namelist = zip_file.namelist()
            members = [name for name in namelist if name.startswith(database_dir)]
            click.echo("📦 Extracting files...")
            zip_file.extractall(tmp_dir, members)

    click.echo("🏗️ Building database...")
    if overwrite and os.path.exists(db_path):
        os.unlink(db_path)

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    sql_script = files.cat_files(tmp_dir + database_dir + "schemas/")
    sql_script += files.cat_files(tmp_dir + database_dir + "data/")

    cursor.executescript(sql_script)
    connection.close()
    click.echo("🆑 Removing temporary files...")
    rmtree(tmp_dir)
    click.echo("✅ Done!")
