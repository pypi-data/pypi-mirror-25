"""
Endpointer CLI

Usage: endpointer [subcommand] [OPTIONS]

Subcommands:
  spec             Work with a specification (linting, validation etc.)
  endpoints        Work with endpoints (discovery, validation, profiling)
  build            Build documentation from a specification. (TODO)
  update           Update documentation from a sepcification. (TODO)

Options:
  --help           Show this message and exit.
  --verbose        Verbose output
"""
from .cli import cli
#from .endpoints import endpoints_command as endpoints
#from .spec import spec_command as spec
from .combine import combine_command as combine
