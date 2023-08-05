import yaml, pyaml, sys
from difflib import Differ
from .cli import command, arg
#from .cli import arg

@command('edit',
    arg('cql', nargs="?", help="SPACE:title, pageID or CQL"),
    arg('-f', '--filter', help="page property filter in format pageprop==value or pageprop!=value", default=None),
    arg('file', nargs="?", help="file to read data from"),
    # need arg_group
    arg('--show', action="store_true", help="show new content"),
    arg('--diff', action="store_true", help="show diff"),
    )
def cmd_edit(config):
    """edit a confluence page using CSS selections

    Pass a dictionary in YAML or JSON format via STDIN or file to
    confluence-tool, which defines edit actions to edit all matching pages.

    """

    confluence = config.getConfluenceAPI()
    first = True

    if not config['file']:
        editor_config = yaml.safe_load(sys.stdout)
    else:
        with open(fn, 'r') as f:
            editor_config = yaml.safe_load(f)

    if 'page' in editor_config:
        cql = confluence.resolveCQL(editor_config.pop('page'))
    if 'cql' in editor_config:
        cql = editor_config.pop('cql')
    if config['cql']:
        cql = config['cql']

    editor = StorageEditor(confluence, **editor_config)

    for page,content in confluence.editPages(config.cql, filter=args.filter, editor=editor):
        if not first:
            print "---"
            first = True

        if args.show:
            p = page.dict('id', 'spacekey', 'title')
            p['content'] = content
            pyaml.p(p)

        elif args.diff:
            p = page.dict('id', 'spacekey', 'title')

            old = page['body']['storage']['value'].splitlines(1)
            new = content.splitlines(1)
            d = Differ()
            result = list(d.compare(old, new))

            p['diff'] = ''.join(result)
            pyaml.p(p)

        else:
            p = page.dict('id', 'spacekey', 'title')
            p['storage'] = content
            version = p['version']['number']

            result = confluence.updatePage(**p)
            pyaml.p(result)
            
