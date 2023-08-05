"""
# Confluence Tool

Confluence Tool is for doing batch operations in confluence.

## Getting Started

For configuration, please run "confluence-tool -b BASE_URL config"

"""
from argdeco import CommandDecorator, arg, mutually_exclusive, group

command = CommandDecorator(
    arg('-c', '--config',      help="Configuration name", default='default'),
    arg('-C', '--config-file', help="Configuratoin file (default ~/.confluence-tool.yaml)"),
    arg('-b', '--baseurl',     help="Confluence Base URL, e.g. http://example.com/confluence"),
    arg('-u', '--username',    help="username for logging in (if not present, tried to read from netrc)"),
    arg('-p', '--password',    help="password for logging in (if not present, tried to read from netrc)"),
    arg('-d', '--debug',       action="store_true", help="get more information on exceptions"),
)

arg_cql = positional_arg_cql = arg('cql', help="SPACE:title, pageID or CQL, run '%(prog)s cql -h' for more help")
positional_optarg_cql = arg('cql', nargs="?", help="SPACE:title, pageID or CQL, '%(prog)s cql -h' for more help")

arg_expand = arg('-e', '--expand', help="values to expand")
arg_filter = arg('-f', '--filter', help="page property filter (name==value or name!=value)")
arg_write_format = arg('-w', '--write', help="format to write", choices=['yaml', 'json'], default="yaml")
arg_format = arg('-F', '--format', help="format string for formatting the output.  May be either mustache or format string")

@command('cql')
def cql_help(config):
    """How to query pages.

    You can pass [CQL] queries to many commands (indicated by parameter cql).
    In many queries you have to specify the ID, which originally needs an extra
    step to find it out.  So there is a convenience syntax for most common
    queries.

    [CQL]: https://developer.atlassian.com/confdev/confluence-server-rest-api/advanced-searching-using-cql

    Here you find a little translation of convenience syntax to CQL:

    - `<QUERY> ">>"` -> `ancestor = <ID of result of QUERY>`
    - `<QUERY> ">"`  -> `parent   = <ID of result of QUERY>`
    - `<SPACE> ":" <TITLE>` -> `space = <SPACE> and title = "<TITLE>"`
    - `":" <TITLE>`   -> `title = "<TITLE>"`
    - `<PAGE_ID>`  -> `ID = <PAGE_ID>`
    - `<PAGE_URI>` -> `ID = <page ID from PAGE_URI>`

    Examples:

     - `"IT:Some title>>"` to find all descendent pages of page with title
       "Some title" in space "IT"

     - `"IT:Some title"` to find page titled "Some title" in space "IT"

    """
    command['cql'].print_help()
