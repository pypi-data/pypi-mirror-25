"""
Endpointer CLI 'endpoints' subcommand

Usage: endpointer endpoints [specification.yml] [OPTIONS]

Options:
  --help           Show this message and exit.
  --verbose        Verbose output

Proposed options:
  --paths          Just list the paths
  --resources      Just list the resources
  --missing        Just list actions that don't belong to an endpoint
"""
import click
from .cli import cli
from ..specification import Specification

@cli.command()
@click.argument('spec_file', type=click.Path(exists=True))
@click.pass_context
def endpoints_command(ctx, spec_file):
    """
    List paths within the specification provided
    """
    if ctx.obj.debug:
        click.secho(
            "Specification: " + click.format_filename(spec_file),
            fg="yellow"
        )

    click.echo("Paths:")
    spec = Specification(spec_file)
    for path in spec.paths():
        click.echo(' '*4 + path)
