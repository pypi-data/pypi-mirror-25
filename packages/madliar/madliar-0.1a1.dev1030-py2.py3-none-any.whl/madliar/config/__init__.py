"""
Settings and configuration for madliar.

"""

import os
import sys
from madliar.exceptions import ProjectFolderStructureError


class SettingsBuilder(type):
    def __new__(mcs, *args):
        name, bases, namespace = args[:]
        try:
            sys.path.append(os.getcwd())
            management = __import__("management.config")
            user_settings = getattr(management, "config")
        except AttributeError:
            sys.stderr.write("Cannot read user's custom settings.")
            raise ProjectFolderStructureError(
                "This error occured because the project folder is not " 
                "in accordance with the rules of madliar, see the detail "
                "at `README.rst`."
            )

        except ImportError:
            from madliar.config import default_settings as user_settings

        namespace["__slots__"] = [_ for _ in dir(user_settings) if not _.startswith("__")]

        def __init__(self):
            for slot in namespace["__slots__"]:
                setattr(self, slot, getattr(user_settings, slot))

        namespace["__init__"] = __init__
        return type.__new__(mcs, name, bases, namespace)


class SettingsLoader(object):
    __metaclass__ = SettingsBuilder


settings = SettingsLoader()
