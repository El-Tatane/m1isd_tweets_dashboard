from my_framework.TemplateBuilder import TemplateBuilder
from my_framework.ModalTemplateBuilder import ModalTemplateBuilder
from my_framework.router import set_route, clean_route, ROUTES
from my_framework.Orchestrator import JOB_RESULTS, set_orchestrator
import json
from DataLoader import DataLoader
from utils import clean_filter_value
from initialization import template_dir
import os
data_loader = DataLoader()


# DECLARE ROUTE behind


@set_route("/")
def route_index(**args):
    template = TemplateBuilder(os.path.join(template_dir, "index.html"))
    mod = ModalTemplateBuilder(os.path.join(template_dir, "modal.html"), "modal_filters", "Sauvegarder")
    
    mod.insert_double_element("h1", "Tweet Filters")
    mod.insert_simple_element("input placeholder='username' id='user_name' type='text'")
    mod.insert_raw_html("<span>  separor : ,  </span>")
    mod.insert_simple_element("br")
    mod.insert_simple_element("input placeholder='Text  use , for several' id='text' type='text'")
    mod.insert_simple_element("br")
    mod.insert_simple_element("input placeholder='Hashtag  use , for several' id='hashtag' type='text'")
    mod.insert_simple_element("br")
    mod.insert_simple_element("input placeholder='Pays  use , for several' id='place_country' type='text'")
    mod.insert_simple_element("br")
    mod.insert_simple_element("input placeholder='Nombre min follower' id='user_followers_count' type='integer'")
    mod.insert_simple_element("br")
    mod.insert_simple_element("input placeholder='Langue  use , for several' id='lang' type='integer'")
    mod.insert_simple_element("br")
    mod.insert_simple_element("input placeholder='Date début' id='ts_start' type='text'")
    mod.insert_double_element("span", " to ")
    mod.insert_simple_element("input placeholder='Date fin' id='ts_end' type='text'")
    mod.insert_raw_html("<div>Format date : jj/mm/aaaa hh:mm</div>")
    mod.insert_simple_element("br")
    mod.insert_simple_element("br")

    template.insert_raw_html("<center><h1>Welcome to tweet Dashboard</h1></center>")
    template.insert_raw_html(mod.link_to_open_model("Modifier les filtres", "id_button_open_modal"))
    template.insert_raw_html('<h2><i>Summary</i></h2>')
    template.insert_raw_html('<div><b>Total tweets :</b> <span id="nb_total_tweet">...</span></div>')
    template.insert_raw_html('<div><b>Total country :</b> <span id="nb_total_country">...</span></div>')
    template.insert_raw_html('<div><b>Total user :</b> <span id="nb_total_user_name">...</span></div>')
    template.insert_raw_html('<div><b>Total language :</b> <span id="nb_total_lang">...</span></div>')
    template.insert_raw_html('<div><b>From</b> <span id="span_ts_start">...</span> <b>to</b> <span id="span_ts_end">...</span></div>')
    template.insert_raw_html('<h2><i>Tweet list</i></h2>')
    template.insert_raw_html('<table border="1"><tr>'
                             '<th>user</th> <th>date</th> <th>text</th>'
                             '</tr><tbody id="table_list_tweet"></tbody></table>')
    template.insert_raw_html("<center>")
    template.insert_raw_html('<a onClick="fill_tweet_contain(\'start\')"> &lt&lt </a>')
    template.insert_raw_html('<a onClick="fill_tweet_contain(\'before\')"> &lt </a>')
    template.insert_raw_html('<span id="span_tweet_navigate_start"> 0 </span>')
    template.insert_raw_html('<span> / </span>')
    template.insert_raw_html('<span id="span_tweet_navigate_max"> 4 </span>')
    template.insert_raw_html('<a onClick="fill_tweet_contain(\'next\')"> &gt </a>')
    template.insert_raw_html('<a onClick="fill_tweet_contain(\'last\')"> &gt&gt </a>')
    template.insert_raw_html("</center>")
    template.insert_raw_html(
        '<h2><i>Language repartition</i></h2>'
        '<canvas id="canvas_pie" width="1500" height="600"> </canvas> '
        '<h2><i>Hashtag repartition</i></h2>'
        '<br> <canvas id="canvas_hist" width="1500" height="800"> </canvas>'
        '<h2><i>Geographic repartition</i></h2>'
        '<br> <canvas id="canvas_map" width="1129" height="846"> </canvas>'
        '<br> <div style = "display:none;">'
        '<img id="source" src="https://www.lri.fr/~kn/teaching/ld/projet/files/world_map.png" length="0" height="0">'
        '</div>'
    )
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
