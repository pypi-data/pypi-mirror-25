"""
Settings and configuration for madliar.

"""

import os
import sys
from madliar import exceptions as mad_exceptions


class SettingsBuilder(type):
    def __new__(mcs, *args):
        name, bases, namespace = args[:]
        try:
            sys.path.append(os.getcwd())
            management = __import__("management.config")
            user_settings = getattr(management, "config")

            slots_dict = {
                slot: getattr(user_settings, slot)
                for slot in dir(user_settings) if not slot.startswith("_")
            }

        except AttributeError:
            sys.stderr.write("Cannot read user's custom settings.")
            raise mad_exceptions.ProjectFolderStructureError(
                "This error occured because the project folder is not " 
                "in accordance with the rules of madliar, see the detail "
                "at `README.rst`."
            )
        except ImportError:
            slots_dict = {}

        # overwrite project default settings
        if "DEBUG" not in slots_dict:
            slots_dict["DEBUG"] = True

        slots_dict["PROJECT_CWD"] = os.path.abspath(".")

        installed_middle_ware = ["madliar.http.middleware.BaseMiddleware"]
        custom_middleware = slots_dict.get("INSTALLED_MIDDLEWARE", [])
        if not isinstance(custom_middleware, (list, tuple)):
            sys.stderr.write(
                "You must regist your middleware in INSTALLED_MIDDLEWARE tuple. not: \n%s"
                % custom_middleware
            )
            sys.exit(0)

        installed_middle_ware.extend(custom_middleware)
        slots_dict["INSTALLED_MIDDLEWARE"] = installed_middle_ware

        if "ENABLE_SYS_LOG" not in slots_dict:
            slots_dict["ENABLE_SYS_LOG"] = True

        if "SYS_LOG_PATH" not in slots_dict:
            slots_dict["SYS_LOG_PATH"] = slots_dict["PROJECT_CWD"]

        if slots_dict["DEBUG"] and "STATICS_URL_MAP" not in slots_dict:
            slots_dict["STATICS_URL_MAP"] = {}

        namespace["__slots__"] = slots_dict.keys()

        def __init__(self):
            for k, v in slots_dict.iteritems():
                setattr(self, k, v)

            def __setattr__(s, key, value):
                raise mad_exceptions.DefaultSettingsWriteError(
                    "Cannot set {%s: %s}, madliar default settings cannot be overwrite."
                    % (key, value)
                )
            self.__class__.__setattr__ = __setattr__

        namespace["__init__"] = __init__
        new_cls = type.__new__(mcs, name, bases, namespace)

        return new_cls


class SettingsLoader(object):
    __metaclass__ = SettingsBuilder


settings = SettingsLoader()
