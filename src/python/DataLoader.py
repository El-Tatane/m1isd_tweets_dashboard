import pandas as pd
import re


class DataLoader:

    def __init__(self, list_path):

        self.df_raw_data = pd.DataFrame()

        for path in list_path:
            df_tweets = pd.read_csv(path, delimiter=",", parse_dates=["date"])
            self.df_raw_data = pd.concat([self.df_raw_data, df_tweets], axis=0, sort=True, ignore_index=True)

    def get_hashtag_tweet_id(self, hashtag):
        """
        return a list of tweet ids which contains the hashtag
        Parameters
        ----------
        hashtag: `str`
            The hashtag of the tweet
         Returns
        -------
        output : `list`
           list of tweet ids
        """
        df = self.raw_data
        return \
            self.raw_data.loc[
                (df['hashtag_0'] == hashtag) | (df['hashtag_1'] == hashtag) | (df['hashtag_0'] == hashtag)][
                'id'].tolist()

    def get_tweet_id(self, value, column_name):
        """
        get tweets of a country, date, user name, id ...
        Parameters
        ----------
        value: `str`, `int`, `float`
            the value that we are looking for (date, country_name, place_name ...)
        Returns
        -------
        output : `list`
            list of ids of the tweets of this user
        """
        return self.raw_data.loc[(self.raw_data[column_name] == value)]['id'].tolist()

    def get_tweet_latitude(self, id):
        """
        return the latitude of a tweet id
        Parameters
        ----------
        id: `int`
            The tweet id
         Returns
        -------
        output : `float`
            latitude
        """
        return self.raw_data.loc[(self.raw_data['id'] == id)]['latitude'][0]

    def get_tweet_longitude(self, id):
        """
        return the longitude of a tweet id
        Parameters
        ----------
        id: `int`
            The tweet id
         Returns
        -------
        output : `float`
            longitude
        """
        return self.raw_data.loc[(self.raw_data['id'] == id)]['longitude'][0]

    def get_user_id_most_or_least_follow(self, most=True):
        """
        return the most follower user id by default else return the least
         Returns
        -------
        output : `str`
            user name
        """
        if most:
            df = self.raw_data.loc[self.raw_data['user_followers_count'].idxmax()]
        else:
            df = self.raw_data.loc[self.raw_data['user_followers_count'].idxmin()]
        return df['user_id']

    def get_user_id_most_or_least_follow_in_country(self, most=True):
        """
         return the id of the user who have the most(by default) or least followers by country
         Parameters
         ----------
        id: `str`
            country name
         Returns
         -------
         output : `DataFrame`
             data frame containing the name of a country, the user id and the count of followers
         """
        df_group_by = self.raw_data.groupby(['place_country'])['user_followers_count']
        idx = df_group_by.transform(max) == self.raw_data['user_followers_count'] if most else df_group_by.transform(
            min) == self.raw_data['user_followers_count']
        return self.raw_data[idx][['place_country', 'user_id', 'user_followers_count']]

    def get_follow_per_country(self, mean_c=False, max_c=False, min_c=False):
        """
         return the mean of followers user by country in ascending order
         Parameters
         ----------
        id: `str`
            country name
         Returns
         -------
         output : `DataFrame`
             data frame containing the name of a country and the mean of followers number
         """
        group_by_country = self.raw_data.groupby(['place_country'])['user_followers_count']
        # df = group_by_country.mean() if mean_c else group_by_country.max() if max_c else group_by_country.min() if min_c else raise Exception(f'change one of the parameters to True')
        if mean_c:
            df = group_by_country.mean()
        elif max_c:
            df = group_by_country.max()
        elif min_c:
            df = group_by_country.min()
        else:
            raise Exception('change one of the parameters of get_user_id_follow_per_country to True')
        return df.reset_index().sort_values('user_followers_count', ascending=False)

    ###############################################################################################################

    def filter_text_equal_tweets(self, df_tweets, column_name, list_word):
        return df_tweets.loc[(df_tweets[column_name].isin(list_word))]

    def filter_text_contain_tweets(self, df_tweets, column_name, list_word):
        fun = lambda x: [i for i in x.split(' ') if i in list_word] != []
        return df_tweets.loc[(df_tweets[column_name].apply(fun))]

    def filter_hashtag_tweets(self, df_tweets, list_word):
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

        if "ts_start" in dict_values.keys() and "ts_end" in dict_values.keys():
            df_filtered_tweets = self.filter_timestamp_tweets(df_filtered_tweets, dict_values["ts_start"],
                                                              dict_values["ts_end"])
        else:
            if "ts_start" in dict_values.keys():
                df_filtered_tweets = self.filter_timestamp_tweets(df_filtered_tweets, ts_min=dict_values["ts_start"])
            elif "ts_end" in dict_values.keys():
                df_filtered_tweets = self.filter_timestamp_tweets(df_filtered_tweets, ts_max=dict_values["ts_end"])

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

    def get_tweet_count(self):
        return 5
