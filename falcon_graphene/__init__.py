"""Implements a GraphQL "best-practice" HTTP service."""
from falcon import HTTPBadRequest

from .decorators import jsonrequest, jsonresponse


class GraphQLResource:
    """http://graphql.org/learn/serving-over-http/"""

    def __init__(self, schema):
        self.schema = schema

    def execute(self, query, context=None):
        return self.schema.execute(query, context_value=context)

    @jsonresponse
    def on_get(self, req, resp):
        query = req.get_param("query", required=True)
        result = self.execute(query, context=req.context)
        return result.data

    @jsonresponse
    @jsonrequest
    def on_post(self, req, resp):
        data = req.context["json"]
        if "query" not in data:
            raise HTTPBadRequest(description="""The "query" parameter is required.""")

        result = self.execute(data["query"], context=req.context)
        return result.data


class GrapheneRouter:
    def __init__(self, schema, resource_kind=GraphQLResource):
        self._schema = schema
        self._resource_kind = resource_kind

    @classmethod
    def from_schema(cls, schema):
        return GrapheneRouter(schema)

    def with_schema(self, schema):
        self._schema = schema
        return self

    def serving_on(self, app, uri="/graphql"):
        self._resource = self._resource_kind(self._schema)
        app.add_route(uri, self._resource)
        return self
