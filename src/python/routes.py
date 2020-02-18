import os

from TemplateBuilder import TemplateBuilder

ROUTES = {}


def clean_route(route):
    if route[0] != "/":
        route = "/" + route
    if route[-1] != "/":
        route += "/"
    return route


# Def decorateur router
def set_route(route):
    if route[0] != "/":
        route = "/" + route
    if route[-1] != "/":
        route += "/"

    def wrapper_set_route(func):
        assert route not in ROUTES.keys(), "REDEFINITON OF EXISTING ROUTE '{}'".format(route)
        ROUTES[route] = func
        return func
    return wrapper_set_route


# DECLARE ROUTE behind

@set_route("/")
def route_index():
    template = TemplateBuilder("index.html")
    template.insert_element("h1", "Titre")
    template.insert_element("p", "coucou")
    return template.get_html()


@set_route("error_404")
def route_404():
    return """<html><head></head><body><h1>ERROR 404</h1></body></html>"""

@set_route("coucou")
def route_coucou():
    return """<html><head></head><body><h1>coucou</h1></body></html>"""



print(ROUTES)