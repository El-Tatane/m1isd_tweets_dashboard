import pandas as pd
import my_framework as mf
from initialization import DICT_CONFIG
from threading import Lock

lock = Lock()


class DataLoader(metaclass=mf.Singleton):

    def __init__(self, list_path=None):
        if list_path is None:
            list_path = []

        self.df_raw_data = pd.DataFrame()
        self.cache = mf.Cache(DICT_CONFIG["cache_size"])

        for path in list_path:
            df_tweets = pd.read_csv(path, delimiter=",", parse_dates=["date"])
            self.df_raw_data = pd.concat([self.df_raw_data, df_tweets], axis=0, sort=True, ignore_index=True)

    def filter_text_equal_tweets(self, df_tweets, column_name, list_word):
        if isinstance(list_word, str):
            list_word = [list_word]
        return df_tweets[df_tweets[column_name].isin(list_word)]

    def filter_text_contain_tweets(self, df_tweets, column_name, list_word):
        fun = lambda x: [i for i in x.split(' ') if i in list_word] != []     # OR
        # fun = lambda x: set(list_word).issubset(x.split(' '))                   # AND
        return df_tweets.loc[(df_tweets[column_name].apply(fun))]

    def filter_hashtag_tweets(self, df_tweets, list_word):
        if isinstance(list_word, str):
            list_word = [list_word]
        return df_tweets.loc[
                (df_tweets['hashtag_0'].isin(list_word)) |
                (df_tweets['hashtag_1'].isin(list_word)) |
                (df_tweets['hashtag_2'].isin(list_word))
            ]

    def filter_user_followers_count_tweets(self, df_tweets, followers_number):
        return df_tweets.loc[(df_tweets["user_followers_count"] >= followers_number)]

    def filter_timestamp_tweets(self, df_tweets, ts_min=None, ts_max=None):
        if ts_min is not None and ts_max is not None:
            return df_tweets.loc[(df_tweets["timestamp"] <= ts_max) & (df_tweets["timestamp"] >= ts_min)]
        else:
            if ts_max is None:
                return df_tweets.loc[(df_tweets["timestamp"] >= ts_min)]
            else:
                return df_tweets.loc[(df_tweets["timestamp"] <= ts_max)]

    def filter_tweets(self, dict_values):
        df_filtered_tweets = self.df_raw_data.copy()

        if "ts_start" in dict_values.keys() or "ts_end" in dict_values.keys():
            df_filtered_tweets = self.filter_timestamp_tweets(df_filtered_tweets, dict_values.get("ts_start", None),
                                                              dict_values.get("ts_end", None))
        if "user_followers_count" in dict_values.keys():
            df_filtered_tweets = self.filter_user_followers_count_tweets(df_filtered_tweets,
                                                                         dict_values["user_followers_count"])
        if "hashtag" in dict_values.keys():
            df_filtered_tweets = self.filter_hashtag_tweets(df_filtered_tweets, dict_values["hashtag"])

        if "text" in dict_values.keys():
            df_filtered_tweets = self.filter_text_contain_tweets(df_filtered_tweets, "text", dict_values["text"])

        for key in ["user_name", "place_country", "lang"]:
            if key in dict_values.keys():
                df_filtered_tweets = self.filter_text_equal_tweets(df_filtered_tweets, key, dict_values[key])
        return df_filtered_tweets

    def get_filter_tweets_with_cache(self, params):
        with lock:  # Care thread problem
            df_data = self.cache.get_cache(params)
            if df_data is None:
                # Cache doesn't exist
                df_data = self.filter_tweets(params)
                self.cache.add_element(params, df_data)
            return df_data.copy()   # return copy to avoid thread problem

    def get_tweet_count(self, params):
        df = self.get_filter_tweets_with_cache(params)
        return df.shape[0]

    def get_country_count(self, params):
        df = self.get_filter_tweets_with_cache(params)
        return df["place_country"].unique().shape[0]

    def get_user_name_count(self, params):
        df = self.get_filter_tweets_with_cache(params)
        return df["user_name"].unique().shape[0]

    def get_lang_count(self, params):
        df = self.get_filter_tweets_with_cache(params)
        return df["lang"].unique().shape[0]

    def get_ts_start(self, params):
        df = self.get_filter_tweets_with_cache(params)
        try:
            return int(df["timestamp"].min()) // 1000
        except:
            return "."      # to avoid bug because of not data

    def get_ts_end(self, params):
        df = self.get_filter_tweets_with_cache(params)
        try:
            return int(df["timestamp"].max()) // 1000
        except:
            return "."      # to avoid bug because of not data

    def get_tweet_contain(self, params, ten_number):
        df = self.get_filter_tweets_with_cache(params)
        df = df.loc[:, ["user_name", "timestamp", "text"]]
        df["timestamp"] = df["timestamp"] / 1000
        return self.filter_ten(df, ten_number).to_dict("records")

    def filter_ten(self, df_data, ten_number):
        # 0 -> 0-9 , 1 -> 10-19 ,  2 -> 20-29
        if ten_number == -1:
            # get last element
            first_index = df_data.shape[0] // 10 * 10
            last_index = df_data.shape[0]
        else:
            first_index = ten_number * 10
            last_index = min(ten_number*10+10, df_data.shape[0])

        if first_index >= df_data.shape[0]:
            return pd.DataFrame()
        return df_data.iloc[first_index: last_index]

    def generic_repartition(self, params, col_name):
        df = self.get_filter_tweets_with_cache(params)
        return df.groupby([col_name]).size().to_dict()

    def hashtag_repartition(self, params):
        df = self.get_filter_tweets_with_cache(params)
        df_0 = df[["hashtag_0"]].dropna().groupby(["hashtag_0"]).size()
        df_1 = df[["hashtag_1"]].dropna().groupby(["hashtag_1"]).size()
        df_2 = df[["hashtag_2"]].dropna().groupby(["hashtag_2"]).size()
        return df_0.add(df_1, fill_value=0).add(df_2, fill_value=0).astype(int).to_dict()

    def country_repartition(self, params):
        df = self.get_filter_tweets_with_cache(params)
        df = df.round({"longitude": 1, "latitude": 1}).groupby(["longitude", "latitude"]).size()
        return [(long, lat, count) for (long, lat), count in df.to_dict().items()]
