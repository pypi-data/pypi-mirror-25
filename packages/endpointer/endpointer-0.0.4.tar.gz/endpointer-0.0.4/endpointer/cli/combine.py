"""
Endpointer CLI 'combine' subcommand.

Combines multiple definitions into a single file.

Usage: endpointer combine [specification.yml] [OPTIONS]

Options:
  --help            Show this message and exit.
  --verbose         Verbose output

Proposed features:  # TODO:
  -o [FILE]         Output to this file insead of stdio
  -y|j              Output in (y)aml and (j)son respectively
                    Deduce output format from -o filename.(extension)
"""

import click
import yaml
from .cli import cli
from ..specification import Specification

@cli.command(name="combine")
@click.argument('spec_file', type=click.Path(exists=True))
@click.pass_context
def combine_command(ctx, spec_file):
    """
    Describes the specification provided.
    """
    if ctx.obj.debug:
        click.secho(
            "Specification: " + click.format_filename(spec_file),
            fg="yellow"
        )
    spec = Specification(spec_file)

    combined_spec_schema = spec.combine().schema()

    # TODO:  If -y, format as yaml

    print(yaml.dump(combined_spec_schema))
