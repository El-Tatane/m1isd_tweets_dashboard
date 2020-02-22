# coding=utf-8
import os

from src.python.my_framework.TemplateBuilder import TemplateBuilder
from src.python.my_framework.router import set_route, clean_route, ROUTES
from src.python.my_framework.Orchestrator import JOB_RESULTS, set_orchestrator


# DECLARE ROUTE behind

@set_route("/")
def route_index(**args):
    template = TemplateBuilder("index.html")
    template.insert_element("h1", "Titre")
    template.insert_element("p", "coucou")
    return template.get_html()


@set_route("error_404")
def route_404(**args):
    template = TemplateBuilder("index.html")
    template.insert_element("h1", "ERREUR 404")
    template.insert_element("p", """Vous avez entrée un lien incorrect""")
    return template.get_html()


@set_route("job/id")
@set_orchestrator()
def route_job_id(**args):
    return str(args)


@set_route("job/result")
def route_job_result(**args):
    return JOB_RESULTS

print(ROUTES)
# print(JOB_RESULTS)
