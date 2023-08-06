"""
Endpointer CLI scripts
"""
import os
import click

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

@cli.command(name="about")
def about():
    """
    Learn more about endpointer
    """
    click.echo(
        """
        Hello! Welcome to endpointer.

        endpointer is a tool for working with OpenAPI specifications.
        We currently target v3. v2 support is welcomed with contribution.

        Run `endpointer --help` for more info.
        """
    )


if __name__ == '__main__':
    about()
