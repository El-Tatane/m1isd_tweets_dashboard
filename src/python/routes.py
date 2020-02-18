import os

from src.python.my_framework.TemplateBuilder import TemplateBuilder
from src.python.my_framework.router import set_route, clean_route, ROUTES


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