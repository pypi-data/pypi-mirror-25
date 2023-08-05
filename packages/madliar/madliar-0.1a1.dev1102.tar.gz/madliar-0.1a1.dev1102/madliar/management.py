import os
import sys

from random import randint
from importlib import import_module
from madliar.utils import get_traceback


__all__ = (
    "reg_command",
    "execute_from_command_line",
)

main_help_text = """
 -------------------------------------------------------------------------
    MadLiar.

    Usage:
        madliar-manage <command> [options]

    Commands:

        create_proj [project_name]
            Create a project on local path. Specify the name of working directory.

        runserver [host:port]
            Running a simple server for debug. Specify the host and port of server.

        help
            Show help for commands.

    Custom commands:
%s
 -------------------------------------------------------------------------
"""

__madliar_command_attr_key = "__madliar_command_%0x___" % randint(0, 0xFFFFFFFF)


def reg_command(name):
    def wrap(f):
        setattr(f, __madliar_command_attr_key, name)
        return f
    return wrap


def _get_command_name(f):
    return getattr(f, __madliar_command_attr_key, None)


class built_in_command(object):
    CommandDoesNotExisted = type("built_in_command__CommandDoesNotExisted", (Exception, ), {})
    __function = {}

    def __init__(self, command):
        self.__command = command

    def __call__(self, func):
        self.__class__.__function[self.__command] = func
        return func

    @classmethod
    def run(cls, command, *args, **kwargs):
        picked_func = cls.__function.get(command)
        if callable(picked_func):
            return picked_func(*args, **kwargs)
        else:
            raise cls.CommandDoesNotExisted


@built_in_command(command="runserver")
def runserver(*args):
    try:
        host, port = args[0].split(":")
        port = int(port)
    except (IndexError, TypeError, ValueError) as e:
        error_msg = "An error happend: %s, use default configured.\n" % str(e)
        sys.stdout.write(error_msg)
        host, port = "0.0.0.0", 8080

    sys.stdout.write("Run madliar wsgi server on %s:%s.\n" % (host, port))
    from madliar.core import wsgi_server
    wsgi_server(host, int(port)).serve_forever()


@built_in_command(command="create_proj")
def create_proj(*args):
    try:
        project_name = args[0]
    except IndexError:
        sys.stderr.write("You must type a folder name.")
        return 0

    import string
    avaliable_name_c = string.letters + string.digits + "_"
    if set(project_name) - set(avaliable_name_c):
        sys.stderr.write("Include special characters.")
        return 0

    try:
        from madliar.config.project_template import (
            default_user_url_map,
            default_wsgi_xml,
            default_wsgi_py,
            default_read_me_for_user,
            default_user_config
        )
        project_folder = os.path.join(os.getcwd(), project_name)
        applicaton_folder = os.path.join(project_folder, "application")
        management_folder = os.path.join(project_folder, "management")

        os.mkdir(project_folder)
        os.mkdir(applicaton_folder)
        os.mkdir(management_folder)

        with open(os.path.join(project_folder, "README.rst"), "ab") as f:
            f.write(default_read_me_for_user)
        with open(os.path.join(applicaton_folder, "__init__.py"), "ab"):
            pass
        with open(os.path.join(applicaton_folder, "urls.py"), "ab") as f:
            f.write(default_user_url_map)
        with open(os.path.join(management_folder, "__init__.py"), "ab"):
            pass
        with open(os.path.join(management_folder, "madliar_uwsgi_socket.xml"), "ab") as f:
            f.write(default_wsgi_xml % (os.path.abspath("."), project_name))
        with open(os.path.join(management_folder, "wsgi.py"), "ab") as f:
            f.write(default_wsgi_py)
        with open(os.path.join(management_folder, "config.py"), "ab") as f:
            f.write(default_user_config)

        sys.stdout.write("Application %s created! " % project_name)
    except Exception as e:
        sys.stderr.write("Application %s not create: %s" % (project_name, e))
        return 0


class ManagementUtility(object):
    """
    Encapsulates the logic of the command tools utilities.

    A ManagementUtility finds out the command in the lib.command.py file
    and run it.
    """
    def __init__(self, argv=None):
        self.argv = argv or sys.argv[:]
        self.prog_name = os.path.basename(self.argv[0])
        self.settings_exception = None

    def show_help_text(self):
        custom_command = ""
        for command, target_fucntion in self.load_custom_command().iteritems():
            custom_command += "\n" + " "*8 + command
            if target_fucntion.__doc__:
                doc_lines = target_fucntion.__doc__.splitlines()
                if doc_lines:
                    command_doc = "".join(
                        ["\n" + " "*12 + line.lstrip(" ") for line in doc_lines]
                    ).rstrip(" \n")
                else:
                    command_doc = "\n            No description."
                custom_command += command_doc + "\n"

        if not custom_command:
            custom_command = (
                "\n        Not found custom command.\n"
                "\n        You can write functions that receive system"
                "\n        arguments and process your own buessess logic,"
                "\n        and put it to `command` directory under your"
                "\n        `application` directory.\n"
            )

        full_help_text = main_help_text % custom_command
        sys.stdout.write(full_help_text)

        return 0

    @staticmethod
    def load_custom_command():
        from madliar.utils import find_all_package

        sys.path.append(".")
        application_path = "application"
        if not os.path.exists(application_path):
            return {}

        all_package = find_all_package(application_path)
        commands = {}

        for package in all_package:
            try:
                m = import_module(package)
            except Exception as e:
                sys.stderr.write(
                    "madliar. \n\n"
                    "An error happend when load custom command: %s.\n%s"
                    % (e, get_traceback())
                )
                sys.exit(0)

            public_attrs = [attr for attr in dir(m) if not attr.startswith("_")]
            for attr in public_attrs:
                command_func = getattr(m, attr)
                if not callable(command_func):
                    continue

                command_name = _get_command_name(command_func)
                if not command_name:
                    continue

                if command_name in commands:
                    sys.stderr.write(
                        "madliar. \n\n"
                        "Found duplicate command name: \"%s\" in `%s`, "
                        "a unique name is required, please check it."
                        % (command_name, package)
                    )
                    sys.exit(0)

                commands[command_name] = command_func

        return commands

    def _execute_custom_command(self, *args):
        target, t_args,  = args[0], args[1:]

        custom_command = self.load_custom_command()
        target_function = custom_command.get(target)
        if not callable(target_function):
            sys.stderr.write("Unknow command: %s, try typing `help` ?" % target)
            return 0

        try:
            return target_function(*t_args)
        except Exception as e:
            sys.stderr.write(
                "An error happend when excute command `%s`:\n    %s"
                % (target, e)
            )
        return 0

    def execute(self):
        """
        Given the command-line arguments, this figures out which subcommand is
        being run, and runs it.
        """
        if len(self.argv) < 2 or self.argv[1] == "help":
            return self.show_help_text()

        try:
            excute_resule = built_in_command.run(*self.argv[1:])
        except built_in_command.CommandDoesNotExisted:
            excute_resule = self._execute_custom_command(*self.argv[1:])

        return excute_resule


def execute_from_command_line(argv=None):
    """
    A simple method that runs a Manager.
    """
    utility = ManagementUtility(argv)
    utility.execute()
