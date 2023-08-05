import sys
import os
import django
from optparse import OptionParser

sys.path.insert(0, os.path.realpath('.'))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "spitzer.settings")

django.setup()

from spitzer import __version__
from spitzer.lib.main import Main

commands = ('migrate', 'show_migrations', 'make_migrations', 'create', 'install', 'rollback')


def main():

    parser = OptionParser()

    parser.add_option(
        "-f", "--file", dest="file_path", help="Path to spitzer.yaml"
    )
    parser.add_option(
        "-p", "--path", dest="path", help="Working dir"
    )
    parser.add_option(
        "-v", "-V", "--version", action="callback", callback=version, help="Show Spitzer's version"
    )

    (options, args) = parser.parse_args()

    command = args[0] if len(args) > 0 else None
    working_dir = options.path if options.path is not None else os.getcwd()
    file_path = options.file_path

    if command not in commands:
        print("Unrecognized command!")
        usage()

    try:
        Main(command, working_dir, file_path).run()
    except BaseException as e:
        print(e)
        sys.exit(1)


def usage():
    print("python spitzer comand [{0}]".format(str(commands)))
    sys.exit()


def version(*params):
    print(__version__)
    sys.exit()

if __name__ == "__main__":
    main()
