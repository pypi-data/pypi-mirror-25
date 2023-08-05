import Niuniu
from typing import List
from werkzeug.exceptions import HTTPException
from werkzeug.wrappers import Response, Request
from werkzeug.routing import Map, Rule


class Server(object):
    def __call__(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __init__(self, route_l: List[Rule]):
        self.url_map = Map(route_l)
        self.response_header = []

    def dispatch_request(self, request):
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            resource = adapter.match()[0]()
            response = Response(getattr(resource, request.method.lower())())
        except AttributeError:
            response = Response("METHOD NOT ALLOWED", status=405)
        except HTTPException as e:
            response = Response(e.name, status=e.code)

        # Set HTTP Headers
        response.headers["Server"] = "Niuniu/" + Niuniu.__version__

        return response
