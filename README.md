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
