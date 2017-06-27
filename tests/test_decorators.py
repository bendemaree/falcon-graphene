import json

import falcon
from falcon import HTTP_200, HTTP_400
from falcon.testing import SimpleTestResource, capture_responder_args

from falcon_graphene.decorators import jsonrequest, jsonresponse

import pytest


@pytest.fixture()
def json_app(app):
    class JSONResponseTestResource(SimpleTestResource):
        @jsonresponse
        def on_get(self, req, resp, **kwargs):
            return {"foo": "bar"}

        @jsonrequest
        @falcon.before(capture_responder_args)
        def on_post(self, req, resp):
            return {}

    resource = JSONResponseTestResource()
    app.app.add_route("/_testing", resource)
    return (resource, app)


def test_jsonresponse_basic(json_app):
    # Given a testing resource and an app
    resource, app = json_app

    # If I make a request to a jsonresponse-decorated endpoint
    resp = app.simulate_get("/_testing")

    # I expect the resposne to be successful
    assert resp.status == HTTP_200

    # I expect my data to be returned as JSON
    assert resp.json == {"foo": "bar"}

    # And for the appropriate content-type header to be set
    assert "application/json" in resp.headers.get("content-type")


def test_jsonrequest_basic(json_app):
    # Given a testing resource and an app
    resource, app = json_app

    # And a JSON payload
    body = {"foo": "bar"}

    # If I make a POST request to a jsonrequest endpoint
    resp = app.simulate_post("/_testing", headers={"Content-Type": "application/json"}, body=json.dumps(body))

    # I exepect success
    assert resp.status == HTTP_200

    # And for my JSON data to be in the handler's request context
    assert resource.captured_req.context["json"] == body


def test_jsonrequest_invalid_payload(json_app):
    # Given a testing resource and an app
    resource, app = json_app

    # And an invalid JSON payload
    body = """{"foo": bar}"""

    # If I make a POST request to a jsonrequest endpoint
    resp = app.simulate_post("/_testing", headers={"Content-Type": "application/json"}, body=body)

    # I exepect a Bad Request response
    assert resp.status == HTTP_400
