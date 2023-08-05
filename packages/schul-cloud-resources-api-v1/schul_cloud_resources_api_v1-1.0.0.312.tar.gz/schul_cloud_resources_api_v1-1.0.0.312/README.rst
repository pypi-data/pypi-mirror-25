schul_cloud_resources_api_v1
============================

The resources API package allows easy access to the Schul-Cloud resources servers.
To get an overview about how the api is defined, please refer to the repository_.

Installation
------------

You can install the package with pip from PyPI_

.. code:: shell

    pip install schul_cloud_resources_api_v1

Accessing the API
-----------------

Suppose, a server runs under http://localhost:8080/v1.
You can use the api to connect to it.
If you do not have a server, you can get a test server from the package
`schul_cloud_resources_server_tests`_.

.. code:: Python

    # import the api classes for access
    from schul_cloud_resources_api_v1 import ApiClient, ResourceApi

    # create the client objects
    url = "http://localhost:8080/v1"
    client = ApiClient(url)
    api = ResourceApi(client)

The ``api`` object gives access to the server.
Here, you can see how to access the api:

.. code:: Python

    # import the resource examples
    from schul_cloud_resources_api_v1.schema import get_valid_examples

    # get a valid resource
    resource = get_valid_examples()[0]
    print(resource)
    
    # add the resource to the server
    response = api.add_resource({"data": {"type": "resource", "attributes": resource}})

    # verify the resource is on the server
    all_my_resssources_on_the_server = [
        _id.id for _id in api.get_resource_ids().data]
    assert response.data.id in all_my_resssources_on_the_server

    # get the resource from the server
    resource_copy = api.get_resource(response.data.id)
    assert resource_copy == resource.data.attributes

    # delete the resource
    api.delete_resource(response.data.id)

Authentication
~~~~~~~~~~~~~~

There are these options for authentication:

- no authentication: this is the default and nothing needs to be done.
- basic authentication: authentication with user name and password
- api-key authentication: a key is supplied to authorize the requests.

The authentication is a global state.
All ``ApiClients`` use this global state.
Thus, you can only authenticate at one API at a time.

.. code:: Python

    import schul_cloud_resources_api_v1.auth as auth

You can remove all authentication. This is the default case.

.. code:: Python

    auth.none()

You can authenticate with username and password. This is `Basic Authentication
<https://en.wikipedia.org/wiki/Basic_access_authentication>`__.

.. code:: Python

    auth.basic("username", "password")

You can authenticate with an api key.

.. code:: Python

    auth.api_key("your-api-key")


Validating Resources
~~~~~~~~~~~~~~~~~~~~

When you use resources, you may want to verify if they have the correct format.
The format is specified in the `resource-schema <https://github.com/schul-cloud/resources-api-v1/tree/master/schemas/resource>`_.
This schema is included in this package.

.. code:: Python

    from schul_cloud_resources_api_v1.schema import (
        get_valid_examples, get_invalid_examples, validate_resource, is_valid_resource
    )

You can test if a resource is valid by calling ``is_valid_resource``

.. code:: Python

    valid_resource = get_valid_examples()[0]
    assert is_valid_resource(valid_resource)

    invalid_resource = get_invalid_examples()[0]
    assert not is_valid_resource(invalid_resource)

If you would like to find out more about why the resource is not valid, you can use `validate_resource`.

.. code:: Python

    validate_resource({'title': 'hello'})

In this example, it results in an error that the `url` property is not present but is required.

.. code:: Python

    jsonschema.exceptions.ValidationError: 'url' is a required property
    
    Failed validating 'required' in schema:
        {'properties': {'contentCategory': {'$ref': '#/definitions/ContentCategory'},
                        'contextUrl': {'$ref': '#/definitions/URL'},
                        'curricula': {'items': {'$ref': '../curriculum/curriculum.json'},
                                      'type': 'array'},
                        'dimensions': {'$ref': '#/definitions/Dimensions'},
                        'duration': {'type': 'number'},
                        'languages': {'description': 'As described in IEEE '
                                                     'LOM, Section 1.3 '
                                                     'http://129.115.100.158/txlor/docs/IEEE_LOM_1484_12_1_v1_Final_Draft.pdf',
                                      'items': {'$ref': '#/definitions/Language'},
                                      'type': 'array'},
                        'licenses': {'items': {'$ref': '../license/license.json'},
                                     'type': 'array'},
                        'mimeType': {'description': 'https://tools.ietf.org/html/rfc2046',
                                     'example': 'text/html',
                                     'type': 'string'},
                        'size': {'format': 'int64', 'type': 'integer'},
                        'thumbnail': {'$ref': '#/definitions/URL'},
                        'title': {'description': 'The title of the resource.',
                                  'example': 'Schul-Cloud',
                                  'type': 'string'},
                        'url': {'$ref': '#/definitions/URL'}},
         'required': ['title',
                      'url',
                      'licenses',
                      'mimeType',
                      'contentCategory',
                      'languages'],
         'type': 'object'}
    
    On instance:
        {'title': 'hello'}

Related Packages
----------------

The `Server Tests <https://github.com/schul-cloud/schul_cloud_resources_server_tests>`_ use this library to test servers implementing the API defined in the repository_.

Further Reading
---------------

- To edit this description, you can edit the `file on Github <https://github.com/schul-cloud/resources-api-v1/tree/master/generators/python_client/README.rst>`__.
  You can use `this editor <http://rst.ninjs.org/>`__.







.. _repository: https://github.com/schul-cloud/resources-api-v1
.. _PyPI: https://pypi.python.org/pypi/schul-cloud-resources-api-v1
.. _schul_cloud_resources_server_tests: https://github.com/schul-cloud/schul_cloud_resources_server_tests
