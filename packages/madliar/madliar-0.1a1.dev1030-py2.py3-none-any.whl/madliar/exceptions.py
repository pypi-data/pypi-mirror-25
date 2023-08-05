"""
Global Django exception and warning classes.

"""


class NoInstalledApplicationError(Exception):
    """
    The exception used when no application installed.
    """
    pass


class ProjectFolderStructureError(Exception):
    """
    The exception used when a bad folder structure found.
    """
    pass


class HTTPResponseWriteError(Exception):
    """
    The exception used for syntax errors during parsing or rendering.
    """
    pass
