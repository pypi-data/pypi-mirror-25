import pytest
import responses
import wola_sdk


@responses.activate
def test_client(url, client, schema):
    assert client._client.schema.get_type(name='Node').name == 'Node'


@responses.activate
def test_query(url, client, schema):
    responses.add(responses.POST, url, json={
        'data': {
            'user': {
                'id': 'test'
            }
        }
    })

    query = '''
{
    user(id: "test") {
        id
    }
}
    '''

    assert client.execute(query)['user']['id'] == 'test'


def test_exception(url, client, schema):
    query = '''
{
    user(id: "test") {
        unknown
    }
}
    '''

    with pytest.raises(wola_sdk.WolaGqlError):
        client.execute(query)
