"""Main entry point"""
import os
import click
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
@click.pass_context
def export(context: click.Context, database: str, model: str):
    """Exports SQL script for Dolibarr modules

    DATABASE: SQLite database file.
    """
    model_switch = {
        "payment_form": dolibarr_functions.get_payment_forms_sql,
        "unit_of_measure": dolibarr_functions.get_units_of_measure_sql,
    }
    function = model_switch[model.lower()]
    response = function(database, context.obj["templates_path"])
    dolibarr_functions.get_units_of_measure_sql(database, context.obj["templates_path"])
    click.echo(f"response: {response}")
