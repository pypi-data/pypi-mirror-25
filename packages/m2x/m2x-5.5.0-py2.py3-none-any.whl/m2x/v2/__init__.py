"""
Python toolkit for the `AT&T M2X API <https://m2x.att.com/developer/documentation/v2/overview>`_.

View the `M2X Python Client README <https://github.com/attm2x/m2x-python/blob/master/README.md>`_ for usage details.

All methods in this client library require an API Key for authentication. There are multiple types of API Keys which
provide granular access to your M2X resources. Please review the `API Keys documentation <https://m2x.att.com/developer/documentation/v2/overview#API-Keys>`_
for more details on the different types of keys available.

If an invalid API Key is utilized, you will receive the following error when calling client methods:

>>> client.method(...)
Traceback (most recent call last):
        ...
requests.exceptions.HTTPError: 401 Client Error: Unauthorized
"""