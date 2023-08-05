from .cli import *
import sys

@command('show',
    positional_arg_cql,
    arg_filter,
    arg_expand,
    arg_write_format,
    arg_format,
    mutually_exclusive(
        arg('--storage', action="store_true", help="convenience for: -e 'body.storage' -F '{body[storage][value]}'"),
        arg('--html', action="store_true", help="convenience for: -e 'body.view' -F '{body[view][value]}'"),
        arg('--ls', action="store_true", help="convenience for: -F '{id} {spacekey} {title}'"),
    ),
    arg('field', nargs="*", help='field to dump')
)
def show(config):
    """show a confluence item

    """
    first = True

    mustache, format, printf = None,None,None

    output_filter = lambda x: x

    if not config.get('format') and not config.get('expand'):
        if config.get('html'):
            config['format'] = '{body[view][value]}'
            config['expand'] = 'body.view'

            from html5print import HTMLBeautifier
            output_filter = lambda x: HTMLBeautifier.beautify(x, 4)

        elif config.get('storage'):
            config['format'] = '{body[storage][value]}'
            config['expand'] = 'body.storage'

            from html5print import HTMLBeautifier
            output_filter = lambda x: HTMLBeautifier.beautify(x, 4)

        elif config.get('ls'):
            config['format'] = '{id}  {spacekey}  {title}'
            config['field'] = ['id', 'spacekey', 'title']

    results = []
    kwargs = config.dict('cql', 'expand', 'filter')
    kwargs['cql'] = config.confluence_api.resolveCQL(kwargs['cql'])

    for page in config.confluence_api.getPages(**kwargs):
        results.append(page.dict(*config['field']))

    if config.get('format'):
        for result in results:
            if '{}' in config['format']:
                fields = [ result[f] for f in config['field'] ]
                print config['format'].format(*fields)

            print output_filter(config['format'].format(**result))

    else:
        if len(results) == 1:
            results = results[0]

        if config['write'] == 'json':
            import json
            json.dump(results, sys.stdout)

        elif config['write'] == 'yaml':
            import pyaml
            pyaml.p(results)
