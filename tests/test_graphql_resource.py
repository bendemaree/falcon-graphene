import json

from falcon import HTTP_200, HTTP_400


def test_graphql_endpoint_get(app, router):
    # Given an empty query
    params = {"query": "{}"}

    # If I make a GET request to my GraphQL endpoint
    resp = app.simulate_get("/graphql", params=params)

    # I expect a successful response
    assert resp.status == HTTP_200


def test_graphql_endpoint_get_without_query(app, router):
    # Given no request parameters
    # If I make a GET request to my GraphQL endpoint
    resp = app.simulate_get("/graphql")

    # I expect a Bad Request HTTP response
    assert resp.status == HTTP_400


def test_graphql_endpoint_json_post(app, router):
    # Given an empty query as a JSON body
    body = {"query": "{ }"}

    # If I make a POST request to my GraphQL endpoint
    resp = app.simulate_post(
        "/graphql",
        headers={"Content-Type": "application/json"},
        body=json.dumps(body)
    )

    # I expect a successful response
    assert resp.status == HTTP_200


def test_graphql_endpoint_json_post_without_query(app, router):
    # Given an empty JSON body
    body = {}

    # If I make a GET request to my GraphQL endpoint
    resp = app.simulate_post(
            "/graphql",
            headers={"Content-Type": "application/json"},
            body=json.dumps(body)
    )

    # I expect a Bad Request HTTP response
    assert resp.status == HTTP_400
