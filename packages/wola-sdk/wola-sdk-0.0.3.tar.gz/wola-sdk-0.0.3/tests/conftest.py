import json
import pytest
import responses

import wola_sdk


@pytest.fixture(scope='module')
def url(request):
    return 'https://gql.test'


@pytest.fixture(scope='module')
def schema(request):
    with open('tests/schema.json') as data:
        return json.load(data)


@responses.activate
@pytest.fixture(scope='module')
def client(request, url, schema):
    responses.add(responses.POST, url, json=schema)
    return wola_sdk.WolaGql(url=url, token='my-token')
