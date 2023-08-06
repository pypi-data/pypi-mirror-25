"""Base Classes for objects on the api"""


class Resource(object):
    """Base class for all resources on API"""
    path = None
    instance = None

    def __init__(self, requester=None):
        self.requester = requester

    def post(self, data=None):
        path = self.path
        if self.uuid:
            path = f'{path}{self.uuid}'
        return self.requester.post(path, data=data)

    def get(self, uuid=None):
        """Get an item based on uuid or filters"""
        path = self.instance.path
        if uuid:
            path = f'{path}{uuid}'
        data = self.requester.get(path)
        return self._parse_to_instance(data)

    def _parse_to_instance(self, data):
        return self.instance(self.requester, **data)


class ListResource(Resource):
    """Class for all resources that have multiple objects"""
    valid_filters = ['pageSize']

    def list(self, filters=None):
        """Get all items on api"""
        filters = self._validate_filters(filters)
        for page in self._get_all_pages(filters):
            for item in page:
                item = self._parse_to_instance(item)
                item.pull_details()
                yield item

    def _validate_filters(self, filters):
        if not filters:
            filters = dict()
        if type(filters) is not dict:
            raise TypeError('Filters should be type dict')

        self.valid_filters.extend(ListResource.valid_filters)
        for key in filters:
            if key not in self.valid_filters:
                raise KeyError(f'Filter ({key}) not a valid filter')
        return filters

    def _get_all_pages(self, filters=None):
        params = {'page': 0, 'pageSize': 100}
        if filters:
            params.update(filters)
        items_returned = 1
        while items_returned:
            page = self.requester.get(
                self.instance.path, params=params
            )
            items_returned = len(page['items'])
            params['page'] += 1
            if items_returned:
                yield page['items']


class InstanceResource(Resource):
    """Class for individual resources"""
    uuid = None

    def __init__(self, requester=None, **params):
        super().__init__(requester)
        self._set_attributes(params)
        self._raw_params = params

    def pull_details(self):
        """
        Pull details from api and update attributes with data
        """
        path = f'{self.path}{self.uuid}'
        data = self.requester.get(path)
        self._set_attributes(data)


    def _set_attributes(self, params):
        """
        Update all attributes of an object
        from a list of properties returned from api
        """
        raise NotImplemented
