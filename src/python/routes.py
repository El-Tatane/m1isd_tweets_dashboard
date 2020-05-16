from my_framework.TemplateBuilder import TemplateBuilder
from my_framework.ModalTemplateBuilder import ModalTemplateBuilder
from my_framework.router import set_route, clean_route, ROUTES
from my_framework.Orchestrator import JOB_RESULTS, set_orchestrator
from DataLoader import DataLoader
import json
from yaml import safe_load
import time
import os



# DECLARE ROUTE behind

@set_route("/")
def route_index(**args):
    template = TemplateBuilder("index.html")
    template.insert_double_element("h1", "Analyse tweet")
    template.insert_raw_html('<input id="search" name="q" type="text" placeholder="Research" />')
    template.insert_raw_html('<button id="search-button" onclick=search()>Tweet research</button>')
    mod = ModalTemplateBuilder("modal.html", "modal_filters", "Sauvegarder")
    mod.insert_double_element("h1", "Filtrer les tweets")
    mod.insert_simple_element("input placeholder='Pseudo' id='user_name' type='text'")
    mod.insert_simple_element("br")
    mod.insert_simple_element("input placeholder='Pays' id='place_country' type='text'")
    mod.insert_simple_element("br")
    mod.insert_simple_element("input placeholder='Nombre min follower' id='user_followers_count' type='integer'")
    mod.insert_simple_element("br")
    mod.insert_simple_element("input placeholder='Langue' id='lang' type='text'")
    mod.insert_simple_element("br")
    mod.insert_simple_element("input placeholder='Date début' id='ts_start' type='datetime-local'")
    mod.insert_double_element("span", " à ")
    mod.insert_simple_element("input placeholder='Date fin' id='ts_end' type='datetime-local'")
    mod.insert_simple_element("br")
    mod.insert_simple_element("input placeholder='Hashtag' id='hashtag' type='text'")
    mod.insert_simple_element("br")
    mod.insert_simple_element("input placeholder='tweet text' id='text' type='text'")
    mod.insert_simple_element("br")
    mod.insert_simple_element("br")
    template.insert_raw_html(mod.link_to_open_model("Modifier les filtres"))
    template.insert_raw_html(mod.get_html())
    template.insert_raw_html(
                             '<canvas id="canvas" width="1500" height="600"> </canvas> '
                             '<br> <canvas id="canvas2" width="1500" height="800"> </canvas>'
                             '<br> <canvas id="canvas3" width="1525" height="900"> </canvas>'
                             '<br> <div style = "display:none;">'        
                             '<img id="source" src="https://www.lri.fr/~kn/teaching/ld/projet/files/world_map.png" length="0" height="0">'
                             '</div>'
                             )

    # template.insert_raw_html('<div style="text-align:center"> <canvas id="canvas2" width="600" height="600"> </canvas>')
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
    #print(type(args["nom"]))
    return str(args)


@set_route("job/result")
def route_job_result(**args):
    return json.dumps(JOB_RESULTS)


@set_route("job/tweet_count")
@set_orchestrator()
def count_tweet(**args):
    #preprare_filter()
    time.sleep(5)
    this_dir = os.path.dirname(__file__)
    with open(os.path.join(this_dir, "../..", "config.yml"), 'r') as stream:
        DICT_CONFIG = safe_load(stream)

    for key, value in args.items():
        args[key] = value.split(',') if ',' in value else [value]

    if "ts_end" in args.keys():
        args["ts_end"] = int(args["ts_end"][0])
    if "ts_start" in args.keys():
        args["ts_start"] = int(args["ts_start"][0])

    data_loader = DataLoader(DICT_CONFIG["list_file_path"])

    df = data_loader.filter_tweets(args)
    print(df)
    # return df.to_json(orient='split')
    print(df.to_json(orient='split'))
    return df.to_json(orient='columns')


# @set_route("job/tweet_count")
# @set_orchestrator()
# def count_tweet(**args):
#     return data_loader.get_tweet_count()


print(ROUTES)
# print(JOB_RESULTS)
