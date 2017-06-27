"""Implements a GraphQL "best-practice" HTTP service."""
from falcon import HTTPBadRequest

import graphene

from .decorators import jsonrequest, jsonresponse


class GraphQLResource:
    """Falcon resource that responds to GraphQL queries made over an HTTP interface.

    This resource takes requests and returns responses as noted in the GraphQL
    `Serving Over HTTP`_ best practices documentation.

    .. _Serving Over HTTP: http://graphql.org/learn/serving-over-http/
    """

    def __init__(self, schema: graphene.Schema):
        self.schema = schema

    def execute(self, query: str, context: dict = None) -> dict:
        """Evaluate the given query and context against a Graphene schema.

        Args:
            query: The GraphQL query to evaluate.
            context: Context to be made available while evaluating the query.

        Returns:
            The result of the GraphQL query.
        """
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
    """Create a router to handle GraphQL requests.

    A router holds a reference to a Graphene schema (a pairing of a query
    and mutation schema) and an optional and an optional resource_type.

    You can initialize a router using the :meth:`.from_schema` factory function.

    Example:
        >>> router = GrapheneRouter.from_schema(my_schema)

    However, if you need to customize the Falcon resource (for example, to add
    a decorator to the handler), you can subclass the included
    :class:`.GraphQLResource` and provide it to the :class:`.GrapheneRouter`
    constructor, then provide your schema using :meth:`.with_schema`.

    Example:
        >>> class MyGraphQLResource(GraphQLResource): pass
        >>> router = GrapheneRouter(resource_type=MyGraphQLResource).with_schema(my_schema)

    Args:
        resource_type: A subclass of :class:`.GraphQLResource`.
    """

    def __init__(self, resource_type: GraphQLResource = GraphQLResource):
        self._resource_type = resource_type

    @classmethod
    def from_schema(cls, schema: graphene.Schema) -> "GrapheneRouter":
        """Create a router with a Graphene schema.

        Args:
            schema: A :class:`graphene.Schema` instance.

        Returns:
            A :class:`.GrapheneRouter` set up with the given schema.
        """
        router = GrapheneRouter()
        return router.with_schema(schema)

    def with_schema(self, schema):
        self._schema = schema
        return self

    def serving_on(self, app, uri="/graphql"):
        self._resource = self._resource_type(self._schema)
        app.add_route(uri, self._resource)
        return self
