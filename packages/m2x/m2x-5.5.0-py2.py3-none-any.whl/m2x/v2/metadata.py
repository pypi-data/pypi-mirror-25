class Metadata(object):
  """ Generic methods for interacting with an M2X resource's Metadata
  """
  def __init__(self, api, **data):
      self.api = api

  def read_metadata(self):
    """ Generic method for a resource's Read Metadata endpoint.

    Example endpoints:

    * `Read Device Metadata <https://m2x.att.com/developer/documentation/v2/device#Read-Device-Metadata>`_
    * `Read Distribution Metadata <https://m2x.att.com/developer/documentation/v2/distribution#Read-Distribution-Metadata>`_
    * `Read Collection Metadata <https://m2x.att.com/developer/documentation/v2/collections#Read-Collection-Metadata>`_

    :return: All of the user defined metadata associated with the resource
    :rtype: dict

    :raises: :class:`~requests.exceptions.HTTPError` if an error occurs when sending the HTTP request
    """
    return self.api.get(self.metadata_path())

  def read_metadata_field(self, field):
    """ Generic method for a resource's Read Metadata Field endpoint.

    Example endpoints:

    * `Read Device Metadata Field <https://m2x.att.com/developer/documentation/v2/device#Read-Device-Metadata-Field>`_
    * `Read Distribution Metadata Field <https://m2x.att.com/developer/documentation/v2/distribution#Read-Distribution-Metadata-Field>`_
    * `Read Collection Metadata Field <https://m2x.att.com/developer/documentation/v2/collections#Read-Collection-Metadata-Field>`_

    :return: The value for the given metadata field of the resource
    :rtype: dict

    :raises: :class:`~requests.exceptions.HTTPError` if an error occurs when sending the HTTP request
    """
    return self.api.get(self.metadata_field_path(field))

  def update_metadata(self, params):
    """ Generic method for a resource's Update Metadata endpoint.

    Example endpoints:

    * `Update Device Metadata <https://m2x.att.com/developer/documentation/v2/device#Update-Device-Metadata>`_
    * `Update Distribution Metadata <https://m2x.att.com/developer/documentation/v2/distribution#Update-Distribution-Metadata>`_
    * `Update Collection Metadata <https://m2x.att.com/developer/documentation/v2/collections#Update-Collection-Metadata>`_

    :param params: The metadata being updated

    :return: The API response, see M2X API docs for details
    :rtype: dict

    :raises: :class:`~requests.exceptions.HTTPError` if an error occurs when sending the HTTP request
    """
    return self.api.put(self.metadata_path(), data=params)

  def update_metadata_field(self, field, value):
    """ Generic method for a resource's Update Metadata Field endpoint.

    Example endpoints:

    * `Update Device Metadata Field <https://m2x.att.com/developer/documentation/v2/device#Update-Device-Metadata-Field>`_
    * `Update Distribution Metadata Field <https://m2x.att.com/developer/documentation/v2/distribution#Update-Distribution-Metadata-Field>`_
    * `Update Collection Metadata Field <https://m2x.att.com/developer/documentation/v2/collections#Update-Collection-Metadata-Field>`_

    :param field: The metadata field to be updated
    :param value: The value to update

    :return: The API response, see M2X API docs for details
    :rtype: dict

    :raises: :class:`~requests.exceptions.HTTPError` if an error occurs when sending the HTTP request
    """
    return self.api.put(self.metadata_field_path(field), data={ "value": value })

  def metadata_field_path(self, field):
    return '%s/%s' % (self.metadata_path(), field)

  def metadata_path(self):
    return self.subpath('/metadata')
