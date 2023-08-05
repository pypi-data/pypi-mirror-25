from sanic.response import json, stream
from sanic.views import HTTPMethodView


View = HTTPMethodView
Json = json
Stream = stream

def Qry(req):
    return req.raw_args or {}

def Doc(req):
    return req.json or {}
