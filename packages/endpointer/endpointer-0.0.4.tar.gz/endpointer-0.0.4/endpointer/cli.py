"""
Endpointer CLI scripts
"""
import os
import click
from endpointer import Specification

class Config(object): #pylint: disable=too-few-public-methods
    """
    Helper class to pass config through the click app.
    """

    def __init__(self, home=None, debug=False):
        self.home = os.path.abspath(home or '.')
        self.debug = debug

@click.group()
@click.option('--debug', is_flag=True)
@click.pass_context
def cli(ctx, debug=False):
    """
    Base application/group. Subcommands 'extend' the options/args.
    """
    ctx.obj = Config(debug=debug)

@cli.command()
@click.pass_context
def about():
    """
    Learn more about endpointer
    """
    click.echo("""Hello! Welcome to endpointer.
    Run `endpointer --help` for more info.""")


@cli.command()
@click.option('--spec', '-s', 'spec_file', type=click.Path(exists=True))
@click.pass_context
def paths(ctx, spec_file):
    """
    List paths within the specification provided
    """
    if ctx.obj.debug:
        click.secho(
            "Specification: " + click.format_filename(spec_file),
            fg="yellow"
        )

    spec = Specification(spec_file)
    spec_paths = spec.paths()
    click.echo(spec_paths)

@cli.command()
@click.option('--spec', '-s', 'spec_file', type=click.Path(exists=True))
@click.pass_context
def info(ctx, spec_file):
    """
    Describes the specification provided.
    """
    if ctx.obj.debug:
        click.secho(
            "Specification: " + click.format_filename(spec_file),
            fg="yellow"
        )
    spec = Specification(spec_file)
    if 'info' in spec:
        version = spec['info']['version']
        title = spec['info']['title']
        spec_license = spec['info']['license']['name'] or 'Unknown'

        banner = f"{title} - {version}. {spec_license} licensed"
        click.secho(banner, fg='green')
    else:
        click.secho(f"No info was found in {spec}.", fg="red")

if __name__ == '__main__':
    cli() #pylint: disable=no-value-for-parameter
