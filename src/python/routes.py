# coding=utf-8
import os

from src.python.my_framework.TemplateBuilder import TemplateBuilder
from src.python.my_framework.ModalTemplateBuilder import ModalTemplateBuilder
from src.python.my_framework.router import set_route, clean_route, ROUTES
from src.python.my_framework.Orchestrator import JOB_RESULTS, set_orchestrator


# DECLARE ROUTE behind

@set_route("/")
def route_index(**args):
    template = TemplateBuilder("index.html")
    template.insert_double_element("h1", "Titre")
    template.insert_double_element("p", "coucou")

    mod = ModalTemplateBuilder("modal.html", "modal_filters", "valideeeee")
    mod.insert_simple_element("input placeholder='pays'")
    mod.insert_simple_element("br")
    mod.insert_simple_element("input placeholder='localisation'")
    mod.insert_simple_element("br")
    mod.insert_simple_element("input placeholder='sexe'")
    mod.insert_simple_element("br")

    template.insert_raw_html(mod.link_to_open_model("ouvre moi"))
    template.insert_raw_html(mod.get_html())
    return template.get_html()


@set_route("error_404")
def route_404(**args):
    template = TemplateBuilder("index.html")
    template.insert_double_element("h1", "ERREUR 404")
    template.insert_double_element("p", """Vous avez entrée un lien incorrect""")
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
