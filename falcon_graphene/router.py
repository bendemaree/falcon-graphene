import graphene

from .handlers import GraphQLResource


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
