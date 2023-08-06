"""
Endpointer CLI 'spec' subcommand.

Information about a specification. Includes:
 - summary information
 - validation
 - linting

Usage: endpointer spec [specification.yml] [OPTIONS]

Options:
  --help           Show this message and exit.
  --verbose        Verbose output

Proposed features: # TODO:
  --info           Just show the informational component
  --validate       Just run the validation
  --lint           Just run the linting component
"""

import click
from .cli import cli
from ..specification import Specification

@cli.command()
@click.argument('spec_file', type=click.Path(exists=True))
@click.pass_context
def spec_command(ctx, spec_file):
    """
    Describes the specification provided.
    """
    if ctx.obj.debug:
        click.secho(
            "Specification: " + click.format_filename(spec_file),
            fg="yellow"
        )
    spec = Specification(spec_file)
    # This is britle as it assumes info fields are defined in the spec.
    if 'info' in spec:
        version = spec['info']['version']
        title = spec['info']['title']
        spec_license = spec['info']['license']['name'] or 'Unknown'

        banner = f"{title} - v{version}.    {spec_license} licensed"
        click.secho(banner, fg='green')
    else:
        click.secho(f"No info was found in {spec}.", fg="red")

    # TODO: Implement linting of a spec.

    # TODO: implement validation of a spec
