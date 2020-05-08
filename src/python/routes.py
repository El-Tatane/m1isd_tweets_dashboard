from my_framework.TemplateBuilder import TemplateBuilder
from my_framework.ModalTemplateBuilder import ModalTemplateBuilder
from my_framework.router import set_route, clean_route, ROUTES
from my_framework.Orchestrator import JOB_RESULTS, set_orchestrator
import json
from DataLoader import DataLoader
from utils import clean_filter_value
import time

data_loader = DataLoader()

# DECLARE ROUTE behind


@set_route("/")
def route_index(**args):
    template = TemplateBuilder("index.html")
    template.insert_double_element("h1", "Analyse tweet")
    template.insert_raw_html('<button id="search-button" onclick=search()>UPDATE</button>')
    template.insert_raw_html('<p id="res">...</p>')
    
    mod = ModalTemplateBuilder("modal.html", "modal_filters", "Sauvegarder")
    mod.insert_double_element("h1", "Filtrer les tweets")
    mod.insert_simple_element("input placeholder='Pseudo' id='user_name' type='text'")
    mod.insert_simple_element("br")
    mod.insert_simple_element("input placeholder='Pays' id='place_country' type='text'")
    mod.insert_simple_element("br")
    mod.insert_simple_element("input placeholder='Nombre min follower' id='user_followers_count' type='integer'")
    mod.insert_simple_element("br")
    mod.insert_simple_element("input placeholder='Langue' id='lang' type='integer'")
    mod.insert_simple_element("br")
    mod.insert_simple_element("input placeholder='Date début' id='ts_start' type='datetime-local'")
    mod.insert_double_element("span", " à ")
    mod.insert_simple_element("input placeholder='Date fin' id='ts_end' type='datetime-local'")
    mod.insert_simple_element("br")
    mod.insert_simple_element("input placeholder='Hashtag' id='hashtag' type='text'")
    mod.insert_simple_element("br")
    mod.insert_simple_element("br")

    template.insert_raw_html(mod.link_to_open_model("Modifier les filtres"))
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
    return json.dumps(JOB_RESULTS)


@set_route("job/tweet_count")
@set_orchestrator()
def count_tweet(**args):
    print("before", args)
    dict_clean_params = clean_filter_value(args)
    print("clean params", dict_clean_params)
    return data_loader.get_tweet_count(dict_clean_params)




# @set_route("job/tweet_count")
# @set_orchestrator()
# def count_tweet(**args):
#     return data_loader.get_tweet_count()


print(ROUTES)
# print(JOB_RESULTS)
