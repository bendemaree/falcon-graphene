import falcon
from falcon import testing

from falcon_graphene import GrapheneRouter

import graphene

import pytest


class RootQuery(graphene.ObjectType):
    foo = graphene.String()


@pytest.fixture()
def app():
    api = falcon.API()
    return testing.TestClient(api)


@pytest.fixture()
def router(app):
    schema = graphene.Schema(query=RootQuery)
    router = GrapheneRouter.from_schema(schema).serving_on(app.app)
    return router
