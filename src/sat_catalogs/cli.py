"""Main entry point"""
import os
import click


@click.group()
@click.argument("database", type=click.File("r"))
@click.pass_context
def cli(context: click.Context, database: click.File):
    """Simple CLI tool to manage SAT's catalog SQL scripts

    Args:
        DATABASE: SQLite database file
    """
    templates_path = os.path.dirname(__file__)
    context.obj = {
        "templates_path": templates_path + "/templates",
        "database": database,
    }


