# coding=utf-8
import os

from my_framework.TemplateBuilder import TemplateBuilder
from my_framework.ModalTemplateBuilder import ModalTemplateBuilder
from my_framework.router import set_route, clean_route, ROUTES
from my_framework.Orchestrator import JOB_RESULTS, set_orchestrator
from DataLoader import DataLoader

# PRE TREATMENT
data_filepath = "D:/Users/zakar/Documents/Mes_Documents_2019_2020/ISD/langages_dynamiques/KN/projetJavaScript" \
                "/m1isd_tweets_dashboard/tweets.csv "
data_loader = DataLoader(data_filepath)


# DECLARE ROUTE behind

@set_route("/")
def route_index(**args):
    template = TemplateBuilder("index.html")
    template.insert_double_element("h1", "Analyse tweet")
    template.insert_raw_html('<input id="search" name="q" type="text" placeholder="Research" />')
    template.insert_raw_html('<button id="search-button" onclick=search()>Tweet research</button>')
    template.insert_raw_html('<p id="res">...</p>')
    
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


"""
@set_route("job/tweet_count")
@set_orchestrator()
def count_tweet(**args):
    return 5
"""


@set_route("job/tweet_count")
@set_orchestrator()
def count_tweet(**args):
    return data_loader.get_tweet_count()


print(ROUTES)
# print(JOB_RESULTS)