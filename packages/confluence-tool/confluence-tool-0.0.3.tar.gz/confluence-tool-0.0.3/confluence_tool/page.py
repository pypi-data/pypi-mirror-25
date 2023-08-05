from .page_properties import get_page_properties

class Page:
    def __init__(self, api, data, expand=None):
        self.api = api
        self.data = data
        if hasattr(expand, 'split'):
            self.expand = set([ s.strip() for s in expand.split(',') ])
        else:
            self.expand = set(expand)

    def update(self):
        self.api.getPage(self.data['id'], expand=self.expand)

    def __getattr__(self, name):
        if name == 'pageProperty':
            self.pageProperty = self.data['pageProperties'] = dict(self.loadPageProperties())
            return self.pageProperty
        raise AttributeError(name)

    def __getitem__(self, name):
        if name == 'pageProperties':
            return self.pageProperty

        if name == 'spacekey':
            return self.data['_expandable']['space'].split("/")[-1]
        else:
            return self.data[name]

        raise KeyError(name)

    def dict(self, *keys):
        '''compose new dictionary from given keys'''
        if not len(keys):
            return self.data

        result = {}
        for key in keys:
            result[key] = self[key]

        return result

    def getPageProperty(self, name, default=None):
        return self.pageProperty.get(name, default)

    def getPageProperties(self, *names):
        for k,v in self.pageProperty.items():
            if len(names):
                if k in names:
                    yield (k,v)
            else:
                yield (k,v)

    def loadPageProperties(self, need_html=False, need_data=False, properties=None, **opts):
        if 'body.view' not in self.expand:
            self.expand.add('body.view')
            self.update()
        html = self.data['body']['view']['value']
        return get_page_properties(html, need_html=need_html, need_data=need_data, properties=properties)
        #self.data['pageProperties'] = dict(get_page_properties(self.data['body']['view']['value']))
