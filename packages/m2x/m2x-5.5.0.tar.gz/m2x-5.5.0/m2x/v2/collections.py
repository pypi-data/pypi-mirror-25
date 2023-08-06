from m2x.v2.resource import Resource
from m2x.v2.devices import Device
from m2x.v2.metadata import Metadata

class CollectionDevice(Device):
    COLLECTION_PATH = 'collections/{collection_id}/devices'


class Collection(Resource, Metadata):
    """ Wrapper for AT&T M2X `Collections API <https://m2x.att.com/developer/documentation/v2/collections>`_
    """
    COLLECTION_PATH = 'collections'
    ITEM_PATH = 'collections/{id}'
    ITEMS_KEY = 'collections'

    def devices(self, **params):
        """ Method for `List Devices from an existing Collection <https://m2x.att.com/developer/documentation/v2/collections#List-Devices-from-an-existing-Collection>`_ endpoint.

        :param params: Query parameters passed as keyword arguments. View M2X API Docs for listing of available parameters.

        :return: List of :class:`.Device` objects
        :rtype: `list <https://docs.python.org/2/library/functions.html#list>`_

        :raises: :class:`~requests.exceptions.HTTPError` if an error occurs when sending the HTTP request
        """
        return CollectionDevice.list(self.api, collection_id=self.id, **params)

    def add_device(self, device_id):
        """ Method for `Add device to collection <https://m2x.att.com/developer/documentation/v2/collections#Add-device-to-collection>`_ endpoint.

        :param device_id: ID of the Device being added to Collection
        :type device_id: str

        :raises: :class:`~requests.exceptions.HTTPError` if an error occurs when sending the HTTP request
        """
        path = self.subpath('/devices/{device_id}'.format(device_id=device_id))
        return self.api.put(path)

    def remove_device(self, device_id):
        """ Method for `Remove device from collection <https://m2x.att.com/developer/documentation/v2/collections#Remove-device-from-collection>`_ endpoint.

        :param device_id: ID of the Device being removed from Collection
        :type device_id: str

        :raises: :class:`~requests.exceptions.HTTPError` if an error occurs when sending the HTTP request
        """
        path = self.subpath('/devices/{device_id}'.format(device_id=device_id))
        return self.api.delete(path)
