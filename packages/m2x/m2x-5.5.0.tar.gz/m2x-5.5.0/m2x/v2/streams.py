from m2x.v2.resource import Resource

class Stream(Resource):
    """ Methods for interacting AT&T M2X Device Streams
    """
    ITEM_PATH = 'devices/{device_id}/streams/{name}'
    COLLECTION_PATH = 'devices/{device_id}/streams'
    ITEMS_KEY = 'streams'
    ID_KEY = 'name'

    def __init__(self, api, device, **data):
        self.device = device
        super(Stream, self).__init__(api, **data)

    def update(self, **attrs):
        """ Method for `Update Data Stream <https://m2x.att.com/developer/documentation/v2/device#Create-Update-Data-Stream>`_ endpoint.

        :param attrs: Query parameters passed as keyword arguments. View M2X API Docs for listing of available parameters.

        :return: The Stream being updated
        :rtype: Stream

        :raises: :class:`~requests.exceptions.HTTPError` if an error occurs when sending the HTTP request
        """
        self.data.update(self.item_update(self.api, self.device, self.name, **attrs))
        return self.data

    def remove(self):
        """ Method for `Delete Data Stream <https://m2x.att.com/developer/documentation/v2/device#Delete-Data-Stream>`_ endpoint.

        :return: The API response, see M2X API docs for details
        :rtype: dict

        :raises: :class:`~requests.exceptions.HTTPError` if an error occurs when sending the HTTP request
        """
        return self.api.delete(self.subpath(""))

    def values(self, **params):
        """ Method for `List Data Stream Values <https://m2x.att.com/developer/documentation/v2/device#List-Data-Stream-Values>`_ endpoint.

        :param params: Query parameters passed as keyword arguments. View M2X API Docs for listing of available parameters.

        :return: The API response, see M2X API docs for details
        :rtype: dict

        :raises: :class:`~requests.exceptions.HTTPError` if an error occurs when sending the HTTP request
        """
        return self.api.get(self.subpath('/values'), params=params)

    def sampling(self, interval, **params):
        """ Method for `Data Stream Sampling <https://m2x.att.com/developer/documentation/v2/device#Data-Stream-Sampling>`_ endpoint.

        :param interval: the sampling interval, see API docs for supported interval types
        :param params: Query parameters passed as keyword arguments. View M2X API Docs for listing of available parameters.

        :return: The API response, see M2X API docs for details
        :rtype: dict

        :raises: :class:`~requests.exceptions.HTTPError` if an error occurs when sending the HTTP request
        """
        params['interval'] = interval
        return self.api.get(self.subpath('/sampling'), params=params)

    def stats(self, **attrs):
        """ Method for `Data Stream Stats <https://m2x.att.com/developer/documentation/v2/device#Data-Stream-Stats>`_ endpoint.

        :param attrs: Query parameters passed as keyword arguments. View M2X API Docs for listing of available parameters.

        :return: The API response, see M2X API docs for details
        :rtype: dict

        :raises: :class:`~requests.exceptions.HTTPError` if an error occurs when sending the HTTP request
        """
        return self.api.get(self.subpath('/stats'), data=attrs)

    def add_value(self, value, timestamp=None):
        """ Method for `Update Data Stream Value <https://m2x.att.com/developer/documentation/v2/device#Update-Data-Stream-Value>`_ endpoint.

        :param value: The updated stream value
        :param timestamp: The (optional) timestamp for the upadted value

        :return: The API response, see M2X API docs for details
        :rtype: dict

        :raises: :class:`~requests.exceptions.HTTPError` if an error occurs when sending the HTTP request
        """
        data = {'value': value}
        if timestamp:
            data['timestamp'] = timestamp
        return self.api.put(self.subpath('/value'), data=data)

    update_value = add_value

    def post_values(self, values):
        """ Method for `Post Data Stream Values <https://m2x.att.com/developer/documentation/v2/device#Post-Data-Stream-Values>`_ endpoint.

        :param values: Values to post, see M2X API docs for details
        :type values: dict

        :return: The API response, see M2X API docs for details
        :rtype: dict

        :raises: :class:`~requests.exceptions.HTTPError` if an error occurs when sending the HTTP request
        """
        return self.api.post(self.subpath('/values'), data={
            'values': values
        })

    def delete_values(self, start, stop):
        """ Method for `Delete Data Stream Values <https://m2x.att.com/developer/documentation/v2/device#Delete-Data-Stream-Values>`_ endpoint.

        :param start: ISO8601 timestamp for starting timerange for values to be deleted
        :param stop: ISO8601 timestamp for ending timerange for values to be deleted

        :return: The API response, see M2X API docs for details
        :rtype: dict

        :raises: :class:`~requests.exceptions.HTTPError` if an error occurs when sending the HTTP request
        """
        return self.api.delete(self.subpath('/values'), data=self.to_server({
            'from': start,
            'end': stop
        }))

    def subpath(self, path):
        return self.item_path(self.name, device_id=self.device.id) + path

    @classmethod
    def list(cls, api, device, **params):
        # Search parameters: query, tags, page, limit
        path = cls.collection_path(device_id=device.id)
        return super(cls, cls).list(api, path=path, itemize_options={
            'device': device
        }, **params)

    @classmethod
    def create(cls, api, device, name, **attrs):
        response = cls.item_update(api, device, name, **attrs)
        return cls.item(api, response, device=device)

    @classmethod
    def get(cls, api, device, id, **params):
        path = cls.item_path(id, device_id=device.id)
        return super(cls, cls).get(api, id, path=path, itemize_options={
            'device': device
        }, **params)

    fetch = get

    @classmethod
    def item_update(cls, api, device, id, **params):
        path = cls.item_path(id, device_id=device.id)
        return super(cls, cls).item_update(api, id, path=path, **params)
