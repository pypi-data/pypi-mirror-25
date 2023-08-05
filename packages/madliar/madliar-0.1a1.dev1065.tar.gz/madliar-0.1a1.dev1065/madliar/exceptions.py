"""
Global exception and warning classes.

"""


class DefaultSettingsWriteError(Exception):
    """
    Default settings is forbidden to overwrite.
    """
    pass


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


class CommandNameRepeatError(Exception):
    """
    The command name must be unique.
    """
    pass
