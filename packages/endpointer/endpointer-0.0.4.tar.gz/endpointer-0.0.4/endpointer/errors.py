"""
Endpointer Errors
"""

class InvalidPointerError(KeyError):
    """
    Thrown when $ref's are badly formatted or cannot be resolved in the schema.
    """
    pass
