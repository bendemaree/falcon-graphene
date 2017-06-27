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
