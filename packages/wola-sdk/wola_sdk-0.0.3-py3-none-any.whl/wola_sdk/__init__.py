"""
wola-sdk
~~~~~~~~~~
Python SDK for Wola Graphql
:copyright: (c) 2017 Wola
"""

import json

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

from graphql.error import GraphQLError


__version__ = '0.0.3'


class WolaGql(object):

    def __init__(self, url, token, timeout=None):
        self.token = token

        self.transport = RequestsHTTPTransport(
            url=url,
            timeout=timeout,
            headers={
                'Authorization': 'Bearer {}'.format(token)
            })

        self._client = Client(
            transport=self.transport,
            fetch_schema_from_transport=True)

    def execute(self, query, **vars):
        try:
            data = self._client.execute(
                document=gql(query),
                variable_values=json.dumps(vars)
            )

        except GraphQLError as err:
            raise WolaGqlError(
                message=err.message,
                body=err.source.body,
                locations=err.locations)

        return data


class WolaGqlError(Exception):

    def __init__(self, message, body=None, locations=None):
        self.body = body
        self.locations = locations
        self.message = message

        super().__init__(message)
