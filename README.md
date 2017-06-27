# falcon-graphene

Helpers for registering [Graphene](http://graphene-python.org/) schemas in [Falcon](https://falcon.readthedocs.io/) as advised by the GraphQL [best practices documentation](http://graphql.org/learn/serving-over-http/) for GraphQL over HTTP.

## Example

In our example, we'll make a small object representing various clocks to use as our schema.

```python
import falcon
import graphene
import falcon_graphene

class Clock(graphene.ObjectType):
    name = graphene.String()


class RootQuery(graphene.ObjectType):
    clock = graphene.Field(Clock)


api = falcon.API()
router = GrapheneRouter.from_schema(schema).serve_on(app)
falcon_graphene.register(api, RootQuery)
```

We can now execute GraphQL queries via a `GET` or `POST` to `/graphql`. These examples use [HTTPie](https://httpie.org):

```
http POST https://example.com/graphql query='{ clock { name } }'
```

**Note**: You can try this out in the [`examples`](https://github.com/bendemaree/falcon-graphene/blob/master/examples) directory.

## What is this?

This is simply a bit of glue to interact with a GraphQL API defined in Graphene with the Falcon API framework. By staying simple and using Falcon's architecture, it can do a few things for you:

- Registers handlers under the standard `/graphql` endpoint
- Allows you to bring all of your existing middleware, request/response handling, etc.
- Pushes the Falcon request context down as the `resolve_*` `context` argument

Some of these (notably customizing request/response handling, if the default response format won't work for you) may require extending the Falcon resource that's set up by default, but the resource class is parameterized and since Falcon resources are just classes, you can override functionality nicely:

```python
from falcon_graphene import GraphQLResource, GrapheneRouter

class CustomGraphQLResource(GraphQLResource):
    def on_options(self, req, resp):
        # Perhaps you need the endpoint to reply to OPTIONS requests
        pass

router = GrapheneRouter(resource_kind=CustomGraphQLResource).with_schema(schema).serving_on(api)
```

## What is this not?

Fancy.

## Testing

Tests use `tox` and `pytest`. To get started, install the testing requirements:

```
pip3 install -U -r requirements/testing.txt
```

Then just run `tox`.
