from cherryontop import get, post
from cherryontop import CherryOnTopError
import json


@get("/foo")
def test():
    return json.dumps({"a": 1})


@post("/foo")
def blam():
    return json.dumps({"b": 2})


@get("/splat")
def busted():
    raise CherryOnTopError("abc", meta={1: 1, "x": "y", "foo": {1: 2}})


# @get("/foo")
# def x():
#     return "a"
