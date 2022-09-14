"""Main entry point"""
import os
import click


@click.group()
@click.pass_context
def cli(context: click.Context):
    """Simple CLI tool to manage SAT's catalog SQL scripts"""
    templates_path = os.path.dirname(__file__)
    context.obj = {"templates_path": templates_path + "/templates"}

