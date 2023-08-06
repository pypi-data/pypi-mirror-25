"""
Utilities for Endpointer CLI
"""

import click

def style_supported_verbs(verbs, known_verbs):
    """
    Prints [GET|POST|PUT|DELETE] using colour highlighting to indicate support
    """
    rtn = []
    for verb in known_verbs:
        if verb in verbs:
            rtn.append(click.style(verb, fg='green'))
        else:
            rtn.append(click.style(verb, fg='white'))

    unknown_verbs = list(set(known_verbs) - set(verbs))
    for verb in unknown_verbs:
        if not verb in known_verbs:
            rtn.append(click.style(verb, fg='red'))
    return rtn
