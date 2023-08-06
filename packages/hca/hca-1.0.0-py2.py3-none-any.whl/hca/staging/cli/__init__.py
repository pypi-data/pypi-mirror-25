from .select_command import SelectCommand
from .list_areas_command import ListAreasCommand


def add_commands(subparsers):
    staging_parser = subparsers.add_parser('staging')
    staging_subparsers = staging_parser.add_subparsers()

    help_parser = staging_subparsers.add_parser('help',
                                                description="Display list of staging commands.")
    help_parser.set_defaults(func=_help)

    select_parser = staging_subparsers.add_parser('select',
                                                  description="Select staging area to which you wish to upload files.")
    select_parser.add_argument('urn_or_alias',
                               help="Full URN of a staging area, or short alias.")
    select_parser.set_defaults(func=SelectCommand)

    list_areas_parser = staging_subparsers.add_parser('areas',
                                                      description="List staging areas I know about.")
    list_areas_parser.set_defaults(func=ListAreasCommand)


def _help(args):
    print("""
hca staging commands:

    help     print this message
    select   select a staging area to use
    areas    list staging areas we know about

Use "hca staging <command> -h" to get detailed command help.
""")
