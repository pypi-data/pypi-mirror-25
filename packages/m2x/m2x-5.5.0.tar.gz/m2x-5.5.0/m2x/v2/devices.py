from m2x.v2.resource import Resource
from m2x.v2.metadata import Metadata
from m2x.v2.streams import Stream
from m2x.v2.keys import Key

# Wrapper for AT&T M2X Device API
# https://m2x.att.com/developer/documentation/v2/device
class Device(Resource, Metadata):
    """ Wrapper for AT&T M2X `Device API <https://m2x.att.com/developer/documentation/v2/device>`_
    """
    COLLECTION_PATH = 'devices'
    ITEM_PATH = 'devices/{id}'
    ITEMS_KEY = 'devices'

    def streams(self):
        """ Method for `List Data Streams <https://m2x.att.com/developer/documentation/v2/device#List-Data-Streams>`_ endpoint.

        :return: List of data streams associated with this device as :class:`.Stream` objects
        :rtype: `list <https://docs.python.org/2/library/functions.html#list>`_

        :raises: :class:`~requests.exceptions.HTTPError` if an error occurs when sending the HTTP request
        """
        return Stream.list(self.api, self)

    def stream(self, name):
        """ Method for `View Data Stream <https://m2x.att.com/developer/documentation/v2/device#View-Data-Stream>`_ endpoint.

        :param name: The name of the Stream being retrieved

        :return: The matching Stream
        :rtype: Stream

        :raises: :class:`~requests.exceptions.HTTPError` if an error occurs when sending the HTTP request
        """
        return Stream.get(self.api, self, name)

    def create_stream(self, name, **params):
        """ Method for `Create/Update Data Stream <https://m2x.att.com/developer/documentation/v2/device#Create-Update-Data-Stream>`_ endpoint.

        :param name: Name of the stream to be created
        :param params: Query parameters passed as keyword arguments. View M2X API Docs for listing of available parameters.

        :return: The newly created Stream
        :rtype: Stream

        :raises: :class:`~requests.exceptions.HTTPError` if an error occurs when sending the HTTP request
        """
        return Stream.create(self.api, self, name, **params)

    def update_stream(self, name, **params):
        """ Method for `Create/Update Data Stream <https://m2x.att.com/developer/documentation/v2/device#Create-Update-Data-Stream>`_ endpoint.

        :param name: Name of the stream to be updated
        :param params: Query parameters passed as keyword arguments. View M2X API Docs for listing of available parameters.

        :return: The Stream being updated
        :rtype: Stream

        :raises: :class:`~requests.exceptions.HTTPError` if an error occurs when sending the HTTP request
        """
        return Stream.item_update(self.api, self, name, **params)

    def keys(self):
        """ Lists Keys associated with this device via the
            `List Keys <https://m2x.att.com/developer/documentation/v2/keys#List-Keys>`_ endpoint.

        :return: List of API keys associated with this device as :class:`.Key` objects
        :rtype: `list <https://docs.python.org/2/library/functions.html#list>`_

        :raises: :class:`~requests.exceptions.HTTPError` if an error occurs when sending the HTTP request
        """
        return Key.list(self.api, device=self.id)

    def create_key(self, **params):
        """ Create an API Key for this Device via the `Create Key <https://m2x.att.com/developer/documentation/v2/keys#Create-Key>`_ endpoint.

        :param params: Query parameters passed as keyword arguments. View M2X API Docs for listing of available parameters.

        :return: The newly created Key
        :rtype: Key

        :raises: :class:`~requests.exceptions.HTTPError` if an error occurs when sending the HTTP request
        """
        return Key.create(self.api, device=self.id, **params)

    def location(self):
        """ Method for `Read Device Location <https://m2x.att.com/developer/documentation/v2/device#Read-Device-Location>`_ endpoint.

        :return: Most recently logged location of the Device, see M2X API docs for details
        :rtype: dict

        :raises: :class:`~requests.exceptions.HTTPError` if an error occurs when sending the HTTP request
        """
        return self.data.get('location') or \
            self.api.get(self.subpath('/location')) or {}

    def location_history(self, **params):
        """ Method for `Read Device Location History <https://m2x.att.com/developer/documentation/v2/device#Read-Device-Location-History>`_ endpoint.

        :param params: Query parameters passed as keyword arguments. View M2X API Docs for listing of available parameters.

        :return: Location history of the Device
        :rtype: dict

        :raises: :class:`~requests.exceptions.HTTPError` if an error occurs when sending the HTTP request
        """
        return self.api.get(self.subpath('/location/waypoints'), params=params)

    def update_location(self, **params):
        """ Method for `Update Device Location <https://m2x.att.com/developer/documentation/v2/device#Update-Device-Location>`_ endpoint.

        :param params: Query parameters passed as keyword arguments. View M2X API Docs for listing of available parameters.

        :return: The API response, see M2X API docs for details
        :rtype: dict

        :raises: :class:`~requests.exceptions.HTTPError` if an error occurs when sending the HTTP request
        """
        return self.api.put(self.subpath('/location'), data=params)

    def delete_location_history(self, **values):
        """ Method for `Delete Device Location History <https://m2x.att.com/developer/documentation/v2/device#Delete-Location-History>`_ endpoint.

        :param values: Query parameters passed as keyword arguments. View M2X API Docs for listing of available parameters.

        :return: The API response, see M2X API docs for details
        :rtype: dict

        :raises: :class:`~requests.exceptions.HTTPError` if an error occurs when sending the HTTP request
        """
        return self.api.delete(self.subpath('/location/waypoints'), **values)

    def log(self):
        """ Method for `View Request Log <https://m2x.att.com/developer/documentation/v2/device#View-Request-Log>`_ endpoint.

        :return: Most recent API requests made against this Device
        :rtype: dict

        :raises: :class:`~requests.exceptions.HTTPError` if an error occurs when sending the HTTP request
        """
        return self.api.get(self.subpath('/log'))

    def post_updates(self, **values):
        """ Method for `Post Device Updates (Multiple Values to Multiple Streams) <https://m2x.att.com/developer/documentation/v2/device#Post-Device-Updates--Multiple-Values-to-Multiple-Streams->`_ endpoint.

        :param values: The values being posted, formatted according to the API docs
        :type values: dict

        :return: The API response, see M2X API docs for details
        :rtype: dict

        :raises: :class:`~requests.exceptions.HTTPError` if an error occurs when sending the HTTP request
        """
        return self.api.post(self.subpath('/updates'), data=values)

    def post_update(self, **values):
        """ Method for `Post Device Update (Single Values to Multiple Streams) <https://m2x.att.com/developer/documentation/v2/device#Post-Device-Update--Single-Values-to-Multiple-Streams->` endpoint.

        :param values: The values being posted, formatted according to the API docs
        :type values: dict

        :return: The API response, see M2X API docs for details
        :rtype: dict

        :raises: :class:`~requests.exceptions.HTTPError` if an error occurs when sending the HTTP request
        """
        return self.api.post(self.subpath('/update'), data=values)

    def values(self, **params):
        """ Method for `List Data Stream Values <https://m2x.att.com/developer/documentation/v2/device#List-Data-Stream-Values>`_ endpoint.

        :param params: Query parameters passed as keyword arguments. View M2X API Docs for listing of available parameters.

        :return: The API response, see M2X API docs for details
        :rtype: dict

        :raises: :class:`~requests.exceptions.HTTPError` if an error occurs when sending the HTTP request
        """
        return self.api.get(self.subpath('/values'), params=params)

    def values_export(self, **params):
        """ Method for `Export Values from all Data Streams of a Device <https://m2x.att.com/developer/documentation/v2/device#Export-Values-from-all-Data-Streams-of-a-Device>`_ endpoint.

        :param params: Query parameters passed as keyword arguments. View M2X API Docs for listing of available parameters.

        :return: The API response, see M2X API docs for details
        :rtype: dict

        :raises: :class:`~requests.exceptions.HTTPError` if an error occurs when sending the HTTP request
        """
        self.api.get(self.subpath('/values/export.csv'), params=params)
        return self.api.last_response

    def values_search(self, **params):
        """ Method for `Search Values from all Data Streams of a Device <https://m2x.att.com/developer/documentation/v2/device#Search-Values-from-all-Data-Streams-of-a-Device>`_ endpoint.

        :param params: Query parameters passed as keyword arguments. View M2X API Docs for listing of available parameters.

        :return: The API response, see M2X API docs for details
        :rtype: dict

        :raises: :class:`~requests.exceptions.HTTPError` if an error occurs when sending the HTTP request
        """
        return self.api.post(self.subpath('/values/search'), data=params)

    def commands(self, **params):
        """ Method for `Device's List of Received Commands <https://m2x.att.com/developer/documentation/v2/commands#Device-s-List-of-Received-Commands>`_ endpoint.

        :param params: Query parameters passed as keyword arguments. View M2X API Docs for listing of available parameters.

        :return: The API response, see M2X API docs for details
        :rtype: dict

        :raises: :class:`~requests.exceptions.HTTPError` if an error occurs when sending the HTTP request
        """
        return self.api.get(self.subpath('/commands'), params=params)

    def command(self, id):
        """ Method for `Device's View of Command Details <https://m2x.att.com/developer/documentation/v2/commands#Device-s-View-of-Command-Details>`_ endpoint.

        :param id: ID of the Command to retrieve

        :return: The API response, see M2X API docs for details
        :rtype: dict

        :raises: :class:`~requests.exceptions.HTTPError` if an error occurs when sending the HTTP request
        """
        return self.api.get(self.subpath('/commands/%s' % id))

    def process_command(self, id, **params):
        """ Method for `Device Marks a Command as Processed <https://m2x.att.com/developer/documentation/v2/commands#Device-Marks-a-Command-as-Processed>`_ endpoint.

        :param id: ID of the Command being marked as processed
        :param params: Optional data to be associated with the processed command, see API docs for details

        :return: The API response, see M2X API docs for details
        :rtype: dict

        :raises: :class:`~requests.exceptions.HTTPError` if an error occurs when sending the HTTP request
        """
        return self.api.post(self.subpath('/commands/%s/process' % id), data=params)

    def reject_command(self, id, **params):
        """ Method for `Device Marks a Command as Rejected <https://m2x.att.com/developer/documentation/v2/commands#Device-Marks-a-Command-as-Rejected>`_ endpoint.

        :param id: ID of the Command being marked as rejected
        :param params: Optional data to be associated with the rejected command, see API docs for details

        :return: The API response, see M2X API docs for details
        :rtype: dict

        :raises: :class:`~requests.exceptions.HTTPError` if an error occurs when sending the HTTP request
        """
        return self.api.post(self.subpath('/commands/%s/reject' % id), data=params)

    @classmethod
    def by_tags(cls, api):
        response = api.get('devices/tags') or {}
        return response.get('tags') or []

    @classmethod
    def catalog(cls, api, **params):
        response = api.get('devices/catalog', **params)
        return cls.itemize(api, response)

    @classmethod
    def search(cls, api, **params):
        response = api.get('devices/search', **params)
        return cls.itemize(api, response)
