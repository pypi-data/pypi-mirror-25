from m2x.v2.resource import Resource

class Key(Resource):
    """ Wrapper for AT&T M2X `Keys API <https://m2x.att.com/developer/documentation/v2/keys>`_
    """
    COLLECTION_PATH = 'keys'
    ITEM_PATH = 'keys/{key}'
    ITEMS_KEY = 'keys'
    ID_KEY = 'key'

    def regenerate(self):
        """ Method for `Regenerate Key <https://m2x.att.com/developer/documentation/v2/keys#Regenerate-Key>`_ endpoint.

        :raises: :class:`~requests.exceptions.HTTPError` if an error occurs when sending the HTTP request
        """
        self.data.update(
            self.api.post(self.item_path(self.key) + '/regenerate')
        )
