# falcon-graphene

Helpers for registering [Graphene](http://graphene-python.org/) schemas in [Falcon](https://falconframework.org/) as advised by the GraphQL [best practices documentation](http://graphql.org/learn/serving-over-http/) for GraphQL over HTTP.

## Example

```python
import falcon

from falcon_graphene import GrapheneRouter

import graphene


class Clock(graphene.ObjectType):
    name = graphene.String()


class RootQuery(graphene.ObjectType):
    clock = graphene.Field(Clock)

    def resolve_clock(self, args, context, info):
        return Clock(name="Charlie")


application = falcon.API()
schema = graphene.Schema(query=RootQuery)
router = GrapheneRouter.from_schema(schema).serving_on(application)
```

**Note**: You can try this out in the [`examples`](https://github.com/bendemaree/falcon-graphene/blob/master/examples) directory.

We can now execute GraphQL queries via a `GET` or `POST` to `/graphql`:

```
http POST :8000/graphql query='{ clock { name } }'
```

**Note**: This example uses [HTTPie](https://httpie.org).

## What is this?

This is simply a bit of glue to interact with a GraphQL API defined in Graphene with the Falcon API framework. By staying simple and using Falcon's architecture, it can do a few things for you:

- Registers handlers under the standard `/graphql` endpoint
- Allows you to bring all of your existing middleware, request/response handling, etc.
- Pushes the Falcon request context down as the `resolve_*` `context` argument

## What is this not?

Fancy.

## Testing

Tests use `tox`To get started, ensure `tox` installed, then just run `tox`.
