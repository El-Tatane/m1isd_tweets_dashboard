import time
import inspect

# twitter created 21 mars 2006 => timestamp = 1142899200
ts_created_twitter = 1142899200 * 1000
ts_now = int(time.time()) * 1000


def clean_special_char(value):
    # dict_replace = {"%20": " ", '"': "%22", "%3C": "<", "%3E": ">"}

    # for before, after in dict_replace.items():
    #     value = value.replace(before, after)
    # return value.decode("ISO-8859-1")
    import urllib
    return urllib.parse.unquote_plus(value) # solve encoding problem


def ts_sec_to_milli(value):
    return value * 1000


def clean_filter_string(value):
    if isinstance(value, list):
        map(lambda x: str(x.strip()), value)
    else:
        value = str(value.strip())
    return value


def clean_filter_int(value):
    try:
        return int(value)
    except ValueError:
        return None


def clean_filter_interval(value, minimum=None, maximum=None):
    if minimum is not None and value < minimum:
        return None
    if maximum is not None and value > maximum:
        return None
    return value


def split_str_to_list(value, sep=",", other_sep=None):
    if other_sep is not None:
        value = value.replace(other_sep, sep)
    return [el for el in value.split(sep) if el != ""]


def clean_filter_value(dict_params):
    res = {}
    dict_all_info_filter = {"user_name": {"fun": [clean_special_char, clean_filter_string]},
                            "place_country": {"fun": [clean_special_char,split_str_to_list, clean_filter_string]},
                            "user_followers_count": {"fun": [clean_special_char, clean_filter_int, clean_filter_interval],
                                                     "params": {"minimum": 0}},
                            "lang": {"fun": [clean_special_char, clean_filter_string]},

                            "ts_start": {"fun": [clean_special_char, clean_filter_int, ts_sec_to_milli, clean_filter_interval],
                                         "params": {"minimum": ts_created_twitter, "maximum": ts_now}},
                            "ts_end": {"fun": [clean_special_char, clean_filter_int,ts_sec_to_milli, clean_filter_interval],
                                       "params": {"minimum": ts_created_twitter, "maximum": ts_now}},
                            "hashtag": {"fun": [clean_special_char, split_str_to_list, clean_filter_string]},
                            "ten_number": {"fun": [clean_special_char, clean_filter_int, clean_filter_interval],
                                           "params": {"minimum": -1}},
                            "text": {"fun": [clean_special_char, split_str_to_list, clean_filter_string],
                                    "params": {"other_sep": " "}}
                            }

    for name, dict_info_filter in dict_all_info_filter.items():
        if name not in dict_params.keys():
            continue

        res[name] = dict_params[name]
        for fun in dict_info_filter["fun"]:
            dict_info_filter["params"] = dict_info_filter.get("params", {})  # fix problem if params doesn't exit
            dict_util_params_for_this_function = {k: v for k, v in dict_info_filter["params"].items() if
                                                  k in [p.name for p in inspect.signature(fun).parameters.values()]}
            res[name] = fun(res[name], **dict_util_params_for_this_function)

            # delete the filter if a value is incorrect
            if res[name] is None:
                res.pop(name)
                break

    return res


if __name__ == "__main__":
    pp = {"user_name": "my username",
          "place_country": "France",
          "user_followers_count": 500,
          "language": "FR",
          "ts_start": "1142899205",
          "ts_end": "1142899209",
          "hashtag": "12"}
    print("res", clean_filter_value(pp))

