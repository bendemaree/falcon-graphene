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
