from m2x.api import HTTPAPIBase
from m2x.v2.collections import Collection
from m2x.v2.commands import Command
from m2x.v2.devices import Device
from m2x.v2.distributions import Distribution
from m2x.v2.jobs import Job
from m2x.v2.keys import Key


class V2Mixin(object):
    """ Wrapper for `AT&T M2X API <https://m2x.att.com/developer/documentation/v2/overview>`_
    """
    PATH = '/v2'

    def status(self):
        """ Returns current status of AT&T M2X API

        :return: Current status of AT&T M2X API
        :rtype: dict
        """
        return self.get('/status')

    def collection(self, id):
        """ Method for `View Collection Details <https://m2x.att.com/developer/documentation/v2/collections#View-Collection-Details>`_ endpoint.

        :param id: ID of the Collection to retrieve
        :type id: str

        :return: The matching Collection
        :rtype: Collection

        :raises: :class:`~requests.exceptions.HTTPError` if an error occurs when sending the HTTP request
        """
        return Collection.get(self, id)

    def create_collection(self, **params):
        """ Method for `Create Collection <https://m2x.att.com/developer/documentation/v2/collections#Create-Collection>`_ endpoint.

        :param params: Query parameters passed as keyword arguments. View M2X API Docs for listing of available parameters.

        :return: The newly created Collection
        :rtype: Collection

        :raises: :class:`~requests.exceptions.HTTPError` if an error occurs when sending the HTTP request
        """
        return Collection.create(self, **params)

    def collections(self, **params):
        """ `List Collections <https://m2x.att.com/developer/documentation/v2/collections#List-collections>`_

        :param params: Query parameters passed as keyword arguments. View M2X API Docs for listing of available parameters.

        :return: List of :class:`.Collection` objects
        :rtype: `list <https://docs.python.org/2/library/functions.html#list>`_

        :raises: :class:`~requests.exceptions.HTTPError` if an error occurs when sending the HTTP request
        """
        return Collection.list(self, **params)

    def command(self, id):
        """ Method for `View Command Details <https://m2x.att.com/developer/documentation/v2/commands#View-Command-Details>`_ endpoint.

        :param id: ID of the Command to retrieve
        :type id: str

        :return: The matching Command
        :rtype: Command

        :raises: :class:`~requests.exceptions.HTTPError` if an error occurs when sending the HTTP request
        """
        return Command.get(self, id)

    def send_command(self, **params):
        """ Method for `Send Command <https://m2x.att.com/developer/documentation/v2/commands#Send-Command>`_ endpoint.

        :param params: Query parameters passed as keyword arguments. View M2X API Docs for listing of available parameters.

        :return: The Command that was just sent
        :rtype: Command

        :raises: :class:`~requests.exceptions.HTTPError` if an error occurs when sending the HTTP request
        """
        return Command.create(self, **params)

    def commands(self, **params):
        """ Method for `List Sent Commands <https://m2x.att.com/developer/documentation/v2/commands#List-Sent-Commands>`_ endpoint.

        :param params: Query parameters passed as keyword arguments. View M2X API Docs for listing of available parameters.

        :return: List of :class:`.Command` objects
        :rtype: `list <https://docs.python.org/2/library/functions.html#list>`_

        :raises: :class:`~requests.exceptions.HTTPError` if an error occurs when sending the HTTP request
        """
        return Command.list(self, **params)

    def device(self, id):
        """ Method for `View Device Details <https://m2x.att.com/developer/documentation/v2/device#View-Device-Details>`_ endpoint.

        :param id: ID of the Device to retrieve
        :type id: str

        :return: The matching Device
        :rtype: Device

        :raises: :class:`~requests.exceptions.HTTPError` if an error occurs when sending the HTTP request
        """
        return Device.get(self, id)

    def create_device(self, **params):
        """ Method for `Create Device <https://m2x.att.com/developer/documentation/v2/device#Create-Device>`_ endpoint.

        :param params: Query parameters passed as keyword arguments. View M2X API Docs for listing of available parameters.

        :return: The newly created Device
        :rtype: Device

        :raises: :class:`~requests.exceptions.HTTPError` if an error occurs when sending the HTTP request
        """
        return Device.create(self, **params)

    def devices(self, **params):
        """ Method for `List Devices <https://m2x.att.com/developer/documentation/v2/device#List-Devices>`_ endpoint.

        :param params: Query parameters passed as keyword arguments. View M2X API Docs for listing of available parameters.

        :return: List of :class:`.Device` objects
        :rtype: `list <https://docs.python.org/2/library/functions.html#list>`_

        :raises: :class:`~requests.exceptions.HTTPError` if an error occurs when sending the HTTP request
        """
        return Device.list(self, **params)

    def devices_search(self, **params):
        """ Method for `Search Devices <https://m2x.att.com/developer/documentation/v2/device#Search-Devices>`_ endpoint.

        :param params: Query parameters passed as keyword arguments. View M2X API Docs for listing of available parameters.

        :return: List of :class:`.Device` objects
        :rtype: `list <https://docs.python.org/2/library/functions.html#list>`_

        :raises: :class:`~requests.exceptions.HTTPError` if an error occurs when sending the HTTP request
        """
        return Device.search(self, **params)

    def device_catalog(self, **params):
        """ Method for `List Public Devices Catalog <https://m2x.att.com/developer/documentation/v2/device#List-Public-Devices-Catalog>`_ endpoint.

        :param params: Query parameters passed as keyword arguments. View M2X API Docs for listing of available parameters.

        :return: List of :class:`.Device` objects
        :rtype: `list <https://docs.python.org/2/library/functions.html#list>`_

        :raises: :class:`~requests.exceptions.HTTPError` if an error occurs when sending the HTTP request
        """
        return Device.catalog(self, **params)

    def device_tags(self, **params):
        """ Method for `List Device Tags <https://m2x.att.com/developer/documentation/v2/device#List-Device-Tags>`_ endpoint.

        :param params: Query parameters passed as keyword arguments. View M2X API Docs for listing of available parameters.

        :return: Device tags associated with your account
        :rtype: dict

        :raises: :class:`~requests.exceptions.HTTPError` if an error occurs when sending the HTTP request
        """
        return Device.by_tags(self, **params)

    def distribution(self, id):
        """ Method for `View Distribution Details <https://m2x.att.com/developer/documentation/v2/distribution#View-Distribution-Details>`_ endpoint.

        :param id: ID of the Distribution to retrieve
        :type id: str

        :return: The matching Distribution
        :rtype: Distribution

        :raises: :class:`~requests.exceptions.HTTPError` if an error occurs when sending the HTTP request
        """
        return Distribution.get(self, id)

    def create_distribution(self, **params):
        """ Method for `Create Distribution <https://m2x.att.com/developer/documentation/v2/distribution#Create-Distribution>`_ endpoint.

        :param params: Query parameters passed as keyword arguments. View M2X API Docs for listing of available parameters.

        :return: The newly created Distribution
        :rtype: Distribution

        :raises: :class:`~requests.exceptions.HTTPError` if an error occurs when sending the HTTP request
        """
        return Distribution.create(self, **params)

    def distributions(self, **params):
        """ Method for `List Distributions <https://m2x.att.com/developer/documentation/v2/distribution#List-Distributions>`_ endpoint.

        :param params: Query parameters passed as keyword arguments. View M2X API Docs for listing of available parameters.

        :return: List of :class:`.Distribution` objects
        :rtype: `list <https://docs.python.org/2/library/functions.html#list>`_

        :raises: :class:`~requests.exceptions.HTTPError` if an error occurs when sending the HTTP request
        """
        return Distribution.list(self, **params)

    def job(self, id):
        """ Method for `View Job Details <https://m2x.att.com/developer/documentation/v2/jobs#View-Job-Details>`_ endpoint.

        :param id: ID of the Job to retrieve
        :type id: str

        :return: The matching Job
        :rtype: Job

        :raises: :class:`~requests.exceptions.HTTPError` if an error occurs when sending the HTTP request
        """
        return Job.get(self, id)

    def key(self, key):
        """ Method for `View Key Details <https://m2x.att.com/developer/documentation/v2/keys#View-Key-Details>`_ endpoint.

        :param id: ID of the Key to retrieve
        :type id: str

        :return: The matching Key
        :rtype: Key

        :raises: :class:`~requests.exceptions.HTTPError` if an error occurs when sending the HTTP request
        """
        return Key.get(self, key)

    def create_key(self, **params):
        """ Method for `Create Key <https://m2x.att.com/developer/documentation/v2/keys#Create-Key>`_ endpoint.

        :param params: Query parameters passed as keyword arguments. View M2X API Docs for listing of available parameters.

        :return: The newly created Key
        :rtype: Key

        :raises: :class:`~requests.exceptions.HTTPError` if an error occurs when sending the HTTP request
        """
        return Key.create(self, **params)

    def keys(self, **params):
        """ Method for `List Keys <https://m2x.att.com/developer/documentation/v2/keys#List-Keys>`_ endpoint.

        :param params: Query parameters passed as keyword arguments. View M2X API Docs for listing of available parameters.

        :return: List of :class:`.Key` objects
        :rtype: `list <https://docs.python.org/2/library/functions.html#list>`_

        :raises: :class:`~requests.exceptions.HTTPError` if an error occurs when sending the HTTP request
        """
        return Key.list(self, **params)

    def time(self):
        """ Method for the `/time <https://m2x.att.com/developer/documentation/v2/time>`_ endpoint.

        :return: The M2X server's current time in seconds, milliseconds and ISO8601 format
        :rtype: dict
        """
        return self.get('/time')

    def time_seconds(self):
        """ Method for the `/time/seconds <https://m2x.att.com/developer/documentation/v2/time>`_ endpoint.

        :return: The M2X server's current time in seconds
        :rtype: int
        """
        return self.get('/time/seconds')

    def time_millis(self):
        """ Method for the `/time/millis <https://m2x.att.com/developer/documentation/v2/time>`_ endpoint.

        :return: The M2X server's current time in milliseconds
        :rtype: int
        """
        return self.get('/time/millis')

    def time_iso8601(self):
        """ Method for the `/time/iso8601 <https://m2x.att.com/developer/documentation/v2/time>`_ endpoint.

        :return: The M2X server's current time in ISO8601 format
        :rtype: str
        """
        return self.get('/time/iso8601').content


class APIVersion2(V2Mixin, HTTPAPIBase):
    pass
