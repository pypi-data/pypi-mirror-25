import sys, re
from .cli import command, arg
import pyaml

@command('page-prop-get',
    arg('cql', help="SPACE:title, pageID or CQL"),
    arg('-f', '--filter', help="page property filter in format pageprop==value or pageprop!=value", default=None),
    arg('props', nargs="*", help="properties to retrieve"),
    )
def cmd_page_prop_get(config):
    """\
    Get page properties.

    For each page there is printed a YAML document with `id`, `title` and
    `spacekey`.  Page properties are printed under `pageProperties`.

    Optionally you can pass some page property filter expressions to filter
    pages on page properties additionally to CQL query.
    """
    confluence = config.getConfluenceAPI()
    first = True

    for pp in confluence.getPagesWithProperties(**config.dict('cql', 'filter')):
        if not first:
            print("---")
        else:
            first = False

        result = pp.dict("id", "spacekey", "title")
        result['pageProperties'] = dict(pp.getPageProperties(*config.props))

        pyaml.p(result)


@command('page-prop-set',
    arg('cql', nargs="?", help="SPACE:title, pageID or CQL"),
    arg('-f', '--filter', help="page property filter in format pageprop==value or pageprop!=value", default=None),
    arg('-p', '--parent', help="specify parent for a page, which might be created"),
    arg('-l', '--label', action="append", help="add these labels to the page"),
    arg('propset', nargs="*", help="property setting expression"),
    arg('file', nargs="*", help="file to read data from")
    )
def cmd_page_prop_set(config):
    """\
    Set page properties.

    # Details

    There are multiple ways of setting page properties.  CQL and page property
    filters are working like in `page-prop-get` command and select pages to
    edit properties.

    # Setting page properties via arguments

    You can add multiple `propset` epressions.  A Propset expression is:

    * `propname:=value` -
      Replace current property with this value.  Value may be JSON or a string.

    * `propname+=value` -
      add value to current property value.

    * `propname-=value` -
      remove value from current property value.

    * `propname--` -
      remove property

    This way default templates for rendering properties are used.


    # Setting page properties via YAML from STDIN

    A document may have following values:

    - `page` - specify a page to be changed
    - `templates` - dictionary of templates with following names:
      - `user` - to render user names.  Gets userkey
      - `page` - to render page Gets spacekey, title
      - `link` - to render link Gets href, caption
      - `list` - to render a list
      - `PROPKEY-TYPE`, where PROPKEY is valid propkey and TYPE is one of the
        above.  This will be used as templates only for that key
    - `pages` - list of documents like this
    - `pagePropertiesEditor` - Define how to change page properties
    """

    confluence = config.getConfluenceAPI()
    first = True

    PROPSET = re.compile(r'^(.*?)([:+-])=(.*)$')
    opmap = {
        ':': 'replace',
        '+': 'add',
        '-': 'remove',
    }

    files = []

    # handle propset
    propset = {}
    for prop in config['propset']:
        if prop.endswith('--'):
            propset[prop[:-2]] = 'delete'
        else:
            m = PROPSET.match(prop)
            if m:
                (name, op, value) = m.groups()
                if name not in propset:
                    propset[name] = {}

                _prop = propset[name]
                op = opmap[op]
                if op not in _prop:
                    _prop[op] = value
                else:
                    if not isinstance(_prop[op], list):
                        _prop[op] = [ _prop[op] ]
                    _prop[op].append(vlaue)

            else:
                files.append(prop)

    # handle filenames
    input = ''
    for filename in files:
        if input != '':
            input += "---\n"
        if filename == '-':
            input += sys.stdin.read()
        else:
            with open(filename, 'r') as f:
                input += f.read()

    documents = []
    # parse yaml multidocument
    if input:
        documents = documents + yaml.safe_load_all(input)

    if len(propset):
        document = {
            'page': config['cql'],
            'pagePropertiesEditor': propset,
        }
        if config.get('parent', None):
            document['parent'] = config['parent']

        documents = [document] + documents
    else:
        if config['cql']:
            if len(documents) == 1:
                documents = [ {
                    'page': config['cql'],
                    'pagePropertiesEditor': documents[0]
                } ]

            if config.get('parent', None):
                documents[0]['parent'] = config['parent']

    labels = config.get('label', [])
    for doc in documents:
        if config.get('parent'):
            if 'parent' not in doc:
                doc['parent'] = config.get('parent')


        for result in confluence.setPageProperties(doc):
            print "updated {}".format(result['result']['id'], )
            if len(labels):
                confluence.addLabels(result['result']['id'], labels)
