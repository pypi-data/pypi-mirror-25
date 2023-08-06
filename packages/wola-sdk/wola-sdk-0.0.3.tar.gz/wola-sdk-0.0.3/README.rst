Wola SDK
========

|Build Status|

Python SDK for Wola GraphQL

Installation
------------

Install from Github.

.. code:: sh

    pip install git+https://github.com/WolaApplication/wola-sdk


Quick start
-----------

**Client**

.. code:: python

    >>> import wola_sdk
    >>> client = wola_sdk.WolaGql(
    ...     url='https://gql.waveapplication.com',
    ...     token='my-token')


**Get node**

.. code:: python

    >>> query = '''
    ... {
    ...   waves(duration_Gte: "30:00") {
    ...     edges {
    ...       node {
    ...         id
    ...         duration
    ...       }
    ...     }
    ...   }
    ... }
    ... '''
    >>> client.execute(query)

**Response**

.. code:: graphql

    {
      "data": {
        "waves": {
          "edges": [
            {
              "node": {
                "id": "V2F2ZU5vZGU6Mg==",
                "duration": "0:45:00"
              }
            }
          ]
        }
      }
    }

**Exception handler**

.. code:: python

    >>> try:
    ...     client.execute(query)
    ... except wola_sdk.WolaGqlError as err:
    ...     print(err.message)


Tests
-----

.. code:: sh

    make test


.. |Build Status| image:: https://drone.waveapplication.com/api/badges/WolaApplication/wola-sdk/status.svg
   :target: https://drone.waveapplication.com/WolaApplication/wola-sdk
