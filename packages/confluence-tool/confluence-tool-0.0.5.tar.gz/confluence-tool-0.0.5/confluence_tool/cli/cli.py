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

positional_arg_cql = arg('cql', help="SPACE:title, pageID or CQL")
positional_optarg_cql = arg('cql', nargs="?", help="SPACE:title, pageID or CQL")

arg_expand = arg('-e', '--expand', help="values to expand")
arg_filter = arg('-f', '--filter', help="page property filter (name==value or name!=value)")
arg_write_format = arg('-w', '--write', help="format to write", choices=['yaml', 'json'], default="yaml")
arg_format = arg('-F', '--format', help="format string for formatting the output.  May be either mustache or format string")
