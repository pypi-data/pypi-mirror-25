import os
import sys


main_help_text = """
 +-------------------------------------------------------------------------+
 |                                                                         |
 | MadLiar.                                                                |
 |                                                                         |
 | Usage:                                                                  |
 |   madliar-manage <command> [options]                                    |
 |                                                                         |
 | Commands:                                                               |
 |   create_proj                 Create a project on local path.           |
 |     [project_name]            Specify the name of working directory.    |
 |                                                                         |
 |   runserver                   Running a simple server for debug.        |
 |     [host:port]               Specify the host and port of server.      |
 |                                                                         |
 |   help                        Show help for commands.                   |
 |                                                                         | 
 |                                                                         |
 +-------------------------------------------------------------------------+
"""


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


@built_in_command(command="help")
def help(*args):
    sys.stdout.write(main_help_text)


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

    def execute(self):
        """
        Given the command-line arguments, this figures out which subcommand is
        being run, and runs it.
        """
        __import__("madliar.config")
        if len(self.argv) < 2:
            help()
            return 0

        try:
            return built_in_command.run(*self.argv[1:])
        except built_in_command.CommandDoesNotExisted:
            # load users command
            sys.stdout.write("Unknown command, type 'help' for usage.")


def execute_from_command_line(argv=None):
    """
    A simple method that runs a Manager.
    """
    utility = ManagementUtility(argv)
    utility.execute()
