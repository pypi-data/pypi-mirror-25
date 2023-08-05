from werkzeug.routing import Rule
from werkzeug.serving import run_simple
from typing import Type
from .resource import Resource
from .server import Server


class App(object):
    def __init__(self):
        self.route_l = []

    def add_resource(self, path: str, resource: Type[Resource]):
        self.route_l.append(Rule(path, endpoint=resource))

    def run(self):
        server = Server(self.route_l)
        run_simple('0.0.0.0', 3773, server, use_debugger=True, use_reloader=True)
