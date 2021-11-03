from typing import Any, Optional

import requests

# output can be
# json | text | none | response

def _request(
    method: str,
    url: str,
    headers=None,
    input: str = "json",
    data: dict = None,
    session: Optional[requests.Session] = None
):
    res = (session or requests).request(
        method,
        url=url,
        json=data if input == "json" else None,
        data=data if input == "form" else None,
        headers=headers,
    )
    return res


def post(
    url: str,
    headers=None,
    input: str = "json",
    output="json",
    data: dict = None,
    session: Optional[requests.Session] = None
):
    res = _request(
        "POST", url,
        headers, input,
        data, session,
    )
    return _handle_res(res, output=output)


def patch(
    url: str,
    headers=None,
    input: str = "json",
    output="json",
    data: dict = None,
    session: Optional[requests.Session] = None
):
    res = _request(
        "PATCH", url,
        headers, input,
        data, session,
    )
    return _handle_res(res, output=output)


def delete(
    url: str,
    headers=None,
    input: str = "json",
    output="json",
    data: dict = None,
    session: Optional[requests.Session] = None
):
    res = _request(
        "DELETE", url,
        headers, input,
        data, session,
    )
    return _handle_res(res, output=output)


def put(
    url: str,
    headers=None,
    input: str = "json",
    output="json",
    data: dict = None,
    session: Optional[requests.Session] = None
):
    res = _request(
        "PUT", url,
        headers, input,
        data, session,
    )
    return _handle_res(res, output=output)


def _handle_res(resp: requests.Response, output):
    if output == "response":
        return resp
    elif output == "none":
        return None
    if resp.ok:
        if output == "json":
            return resp.json()
        else:
            return resp.text


def get(
    url: str,
    output="json",
    headers=None,
    session: Optional[requests.Session] = None
):
    res = (session or requests).get(url, headers=headers)
    return _handle_res(res, output=output)


def get_ping(
    url: str,
    headers=None,
    session: Optional[requests.Session] = None
):
    res = (session or requests).get(url, headers=headers)
    return res.ok


def contains(input: str, inside: str) -> bool:
    return inside in input


def pick(input: dict, key: str) -> Any:
    return input.__getattribute__(key)


def equal(a: Any, b: Any):
    return a == b

def not_equal(a: Any, b: Any):
    return a != b

functions = {
    "http.get": get,
    "http.post": post,
    "http.put": put,
    "http.delete": delete,
    "http.patch": patch,

    "http.ping_get": get_ping,

    # basic utils
    "pick": pick,
    "contains": contains,
    "equal": equal,
    "not_equal": not_equal,
}
