import os
import sys


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
        print "self.argv: %s" % self.argv

    def main_help_text(self):
        """
        Returns the script's main help text, as a string.
        """
        return ""

    def execute(self):
        """
        Given the command-line arguments, this figures out which subcommand is
        being run, and runs it.
        """
        try:
            subcommand = self.argv[1]
        except IndexError:
            subcommand = 'runserver'  # Display help if no arguments were given.

        if subcommand == "runserver":
            try:
                host, port = self.argv[2].split(":")
            except (IndexError, TypeError) as e:
                error_msg = "An error happend: %s, use default configured.\n" % str(e)
                sys.stdout.write(error_msg)
                host, port = "0.0.0.0", 8080

            sys.stdout.write("run as simple wsgi server on %s:%s.\n" % (host, port))
            from madliar.core import wsgi_server
            wsgi_server(host, int(port)).serve_forever()

        else:
            from lib import command
            try:
                return getattr(command, subcommand)(*self.argv[2:])
            except AttributeError:
                sys.stderr.write("Unknown command: '%s' \nType 'help' for usage." % subcommand)


def execute_from_command_line(argv=None):
    """
    A simple method that runs a Manager.
    """
    utility = ManagementUtility(argv)
    utility.execute()
