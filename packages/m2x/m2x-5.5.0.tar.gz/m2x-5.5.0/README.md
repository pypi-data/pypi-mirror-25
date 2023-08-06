# AT&T's M2X Python Client

[![Documentation Status](https://readthedocs.org/projects/m2x-python/badge/?version=latest)](http://m2x-python.readthedocs.io/en/latest/?badge=latest)

[AT&T M2X](http://m2x.att.com) is a cloud-based fully managed time-series data storage service for network connected machine-to-machine (M2M) devices and the Internet of Things (IoT).

The [AT&T M2X API](https://m2x.att.com/developer/documentation/overview) provides all the needed operations and methods to connect your devices to AT&T's M2X service. This library aims to provide a simple wrapper to interact with the AT&T M2X API for [Python](https://www.python.org). Refer to the [Glossary of Terms](https://m2x.att.com/developer/documentation/glossary) to understand the nomenclature used throughout this documentation.

Documentation for the AT&T M2X Python Client Library can be found [here](http://m2x-python.readthedocs.io/en/latest/), though you should also read this README thoroughly before getting started.

Getting Started
===============

1. Signup for an [M2X Account](https://m2x.att.com/signup).
2. Obtain your _Master Key_ from the Master Keys tab of your [Account
   Settings](https://m2x.att.com/account) screen.
3. Create your first [Device](https://m2x.att.com/devices) and copy its _Device
   ID_.
4. Review the [M2X API
   Documentation](https://m2x.att.com/developer/documentation/overview).


## Description

This library provides an interface to navigate and register your data source
values with the [AT&T's M2X service](https://m2x.att.com/), while supporting
Python 2 and 3.


## Dependencies

* [requests](http://www.python-requests.org)
* [iso8601](https://pypi.python.org/pypi/iso8601)

To use Python on your local machine, you'll need to first install
`Python-setuptools`.


## Installation

The project is very easy to install — the different options are:

```bash
$ pip install m2x
```

or:

```bash
$ easy_install m2x
```

or cloning the repository:

```bash
$ git clone https://github.com/attm2x/m2x-python.git
$ cd m2x-python
$ python setup.py install
```

Note: If you are installing from behind a proxy, `setup.py` may have trouble
connecting to the PyPI server to download dependencies. In this case, you'll
need to set the following environment variables to let the setup script know
how to navigate your proxy:

```bash
HTTP_PROXY=http://proxyserver:port/
HTTPS_PROXY=https://proxyserver:ssl_port/
```

## Usage

In order to communicate with the M2X API, you need an instance of
[M2XClient](m2x/client.py). You need to pass your Master API key in the
constructor to access your data. Your Master API Key can be found in your
account settings.

```python
from m2x.client import M2XClient

client = M2XClient(key='<API-KEY>')
```

This `client` an interface to your data in M2X

- [Distributions](m2x/v2/distributions.py)
  ```python
  distribution = client.distribution('<DISTRIBUTION-ID>')
  distributions = client.distributions()
  ```

- [Devices](m2x/v2/devices.py)
  ```python
  device = client.device('<DEVICE-ID>')
  devices = client.devices()
  ```

- [Jobs](m2x/v2/jobs.py)
  ```python
  job = client.job('<JOB-ID>')
  ```

- [Key](m2x/v2/keys.py)
  ```python
  key = client.key('<KEY-TOKEN>')
  keys = client.keys()
  ```

## Examples

Scripts demonstrating usage of the M2X Python Client Library can be found in the [examples](/examples) directory. Each example leverages system environment variables to inject user specific information such as the M2X `API Key` or `Device ID`. Review the example you would like to try first to determine which environment variables are required (hint: search for `os.environ` in the example). Then make sure to set the required environment variable(s) when running the script.

For example, in order to run the [post_value](/examples/post_value.py) script, you will need an `API Key`. After adding your API Key to the `post_value.py` file, navigate to the `/examples` directory and run the following command to execute the script:

```bash
$ API_KEY=<YOUR-API-KEY> python ./post_value.py
```

## Getting HTTP Response

You can retrieve the last response received by the client using the
`last_response` property of the `client` object:

```python
import os
from m2x.client import M2XClient

# Instantiate a client
client = M2XClient(key=os.environ['API_KEY'])

# Make a request to the M2X API
client.devices()

# Get raw HTTP response
raw = client.last_response.raw

# Get HTTP respose status code (e.g. `200`)
status = client.last_response.status

# Get HTTP response headers
headers = client.last_response.headers

# Get json data returned in HTTP response
json = client.last_response.json
```

In the case of an HTTP error response (like a `400` or `500` error),
the library will drop an `HTTPError` exception (inherited from
`python-requests`). You can still retrieve the original respone by
catching this exception:

```python
import os

from requests.exceptions import HTTPError


from m2x.client import M2XClient

# Instantiate a client
client = M2XClient(key=os.environ['API_KEY'])

# Make a request to the M2X API
try:
    client.devices()
except HTTPError as error:
    # Get raw HTTP response
    raw = client.last_response.raw

    # Or get it from the error instance
    # raw = error.response

    # Get HTTP respose status code (e.g. `200`)
    status = client.last_response.status

    # Get HTTP response headers
    headers = client.last_response.headers

    # Get json data returned in HTTP response (might be None)
    json = client.last_response.json
```

## Versioning

This lib aims to adhere to [Semantic Versioning 2.0.0](http://semver.org/). As
a summary, given a version number `MAJOR.MINOR.PATCH`:

1. `MAJOR` will increment when backwards-incompatible changes are introduced to
   the client.
2. `MINOR` will increment when backwards-compatible functionality is added.
3. `PATCH` will increment with backwards-compatible bug fixes.

Additional labels for pre-release and build metadata are available as
extensions to the `MAJOR.MINOR.PATCH` format.

**Note**: the client version does not necessarily reflect the version used in
          the AT&T M2X API.

## License

This library is released under the MIT license. See [LICENSE](LICENSE) for the terms.
