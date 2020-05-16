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
    # template.insert_raw_html('<button id="button_update" onclick=update_all()>UPDATE</button>')
    template.insert_raw_html('<div>Total tweets : <span id="nb_total_tweet">...</span></div>')
    template.insert_raw_html('<div>Total country : <span id="nb_total_country">...</span></div>')
    template.insert_raw_html('<div>Total user : <span id="nb_total_user_name">...</span></div>')
    template.insert_raw_html('<div>Total language : <span id="nb_total_lang">...</span></div>')
    template.insert_raw_html('<div>From <span id="span_ts_start">...</span> to <span id="span_ts_end">...</span></div>')
    template.insert_raw_html('<div>List tweet :</div>')
    template.insert_raw_html('<table border="1"><tr>'
                             '<th>user</th> <th>date</th> <th>text</th>'
                             '</tr><tbody id="table_list_tweet"></tbody></table>')
    template.insert_raw_html('<a onClick="fill_tweet_contain(\'start\')"> &lt&lt </a>')
    template.insert_raw_html('<a onClick="fill_tweet_contain(\'before\')"> &lt </a>')
    template.insert_raw_html('<span id="span_tweet_navigate_start"> 0 </span>')
    template.insert_raw_html('<span> / </span>')
    template.insert_raw_html('<span id="span_tweet_navigate_max"> 4 </span>')
    template.insert_raw_html('<a onClick="fill_tweet_contain(\'next\')"> &gt </a>')
    template.insert_raw_html('<a onClick="fill_tweet_contain(\'last\')"> &gt&gt </a>')

    mod = ModalTemplateBuilder("modal.html", "modal_filters", "Sauvegarder")
    mod.insert_double_element("h1", "Filtrer les tweets")
    mod.insert_simple_element("input placeholder='Pseudo' id='user_name' type='text'")
    mod.insert_simple_element("br")
    mod.insert_simple_element("input placeholder='Text' id='text' type='text'")
    mod.insert_simple_element("br")
    mod.insert_simple_element("input placeholder='Hashtag' id='hashtag' type='text'")
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
    mod.insert_simple_element("br")

    template.insert_simple_element("br")
    template.insert_raw_html(mod.link_to_open_model("Modifier les filtres", "id_button_open_modal"))
    template.insert_raw_html(mod.get_html())
    return template.get_html()


@set_route("error_404")
def route_404(**args):
    template = TemplateBuilder("index.html")
    template.insert_double_element("h1", "ERREUR 404")
    template.insert_double_element("p", """Vous avez entrée un lien incorrect""")
    return template.get_html()


# @set_route("job/id")
# @set_orchestrator()
# def route_job_id(**args):
#     return str(args)


@set_route("job/result")
def route_job_result(**args):
    return json.dumps(JOB_RESULTS)


@set_route("job/tweet_count")
@set_orchestrator()
def tweet_count(**args):
    dict_clean_params = clean_filter_value(args)
    return data_loader.get_tweet_count(dict_clean_params)


@set_route("job/country_count")
@set_orchestrator()
def country_count(**args):
    dict_clean_params = clean_filter_value(args)
    return data_loader.get_country_count(dict_clean_params)


@set_route("job/user_name_count")
@set_orchestrator()
def user_name_count(**args):
    dict_clean_params = clean_filter_value(args)
    return data_loader.get_user_name_count(dict_clean_params)


@set_route("job/lang_count")
@set_orchestrator()
def lang_count(**args):
    dict_clean_params = clean_filter_value(args)
    return data_loader.get_lang_count(dict_clean_params)


@set_route("job/ts_start")
@set_orchestrator()
def ts_start(**args):
    dict_clean_params = clean_filter_value(args)
    return data_loader.get_ts_start(dict_clean_params)


@set_route("job/ts_end")
@set_orchestrator()
def ts_start(**args):
    dict_clean_params = clean_filter_value(args)
    return data_loader.get_ts_end(dict_clean_params)


@set_route("job/tweet_contain")
@set_orchestrator()
def tweet_contain(**args):
    dict_clean_params = clean_filter_value(args)
    ten_number = dict_clean_params.pop("ten_number")
    return data_loader.get_tweet_contain(dict_clean_params, ten_number)

@set_route("job/country_repartition")
@set_orchestrator()
def country_repartition(**args):
    dict_clean_params = clean_filter_value(args)
    return data_loader.country_repartition(dict_clean_params)

@set_route("job/lang_repartition")
@set_orchestrator()
def language_repartition(**args):
    dict_clean_params = clean_filter_value(args)
    return data_loader.generic_repartition(dict_clean_params, "lang")

@set_route("job/hashtag_repartition")
@set_orchestrator()
def hashtag_repartition(**args):
    dict_clean_params = clean_filter_value(args)
    print(dict_clean_params)
    return data_loader.hashtag_repartition(dict_clean_params)

print(ROUTES)
# print(JOB_RESULTS)
