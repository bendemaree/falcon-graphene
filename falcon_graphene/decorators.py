import json

from functools import wraps

from falcon import HTTPBadRequest


def jsonrequest(h):
    """Parse and inject JSON request data into the request context.
    """
    @wraps(h)
    def wrapper(self, req, resp, *args, **kwargs):
        try:
            req.context["json"] = json.load(req.bounded_stream)
        except json.JSONDecodeError:
            raise HTTPBadRequest(description="failed to decode JSON payload")
        return h(self, req, resp, *args, **kwargs)
    return wrapper


def jsonresponse(h):
    """Render a JSON response from the return value of a handler.
    """
    @wraps(h)
    def wrapper(self, req, resp, *args, **kwargs):
        data = h(self, req, resp, *args, **kwargs)
        if data:
            resp.body = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    return wrapper
