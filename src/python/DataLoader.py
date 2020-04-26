import pandas as pd
import re


class DataLoader:

    def __init__(self, list_path):

        self.df_raw_tweets = pd.DataFrame()

        for path in list_path:
            # df_tweets = pd.read_csv(path, parse_dates=['date'])
            df_tweets = pd.read_csv(path, delimiter=";")
            self.df_raw_data = pd.concat([self.df_raw_tweets, df_tweets], axis=0, sort=True, ignore_index=True)


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
    def get_others_tweet_id(self, objects, column_name):
        values = objects.split(',')
        # if column_name == "text":
        #     return self.raw_data.loc[(re.search(self.raw_data[column_name],))]['id'].tolist()
        return self.raw_data.loc[(self.raw_data[column_name].isin(values))]['id'].tolist()

    def get_hashtag_tweet_id(self, objects):
        """
        return a list of tweet ids which contains the hashtag
        Parameters
        ----------
         Returns
        -------
        output : `list`
           list of tweet ids
        """
        df = self.raw_data
        values = objects.split(',')
        return \
            self.raw_data.loc[
                (df['hashtag_0'].isin(values)) | (df['hashtag_1'].isin(values)) | (df['hashtag_0'].isin(values))][
                'id'].tolist()

    def get_followers_tweet_id(self, followers):
        return self.raw_data.loc[(self.raw_data["user_followers_count"] >= followers)]['id'].tolist()

    def get_timestamp_tweet_id(self, ts_min=None, ts_max=None):
        if ts_min is not None and ts_max is not None:
            return self.raw_data.loc[(self.raw_data["timestamp"] <= ts_max) & (self.raw_data["timestamp"] >= ts_min)][
                'id'].tolist()
        else:
            if ts_max is None:
                return self.raw_data.loc[(self.raw_data["timestamp"] >= ts_min)]['id'].tolist()
            else:
                return self.raw_data.loc[(self.raw_data["timestamp"] <= ts_max)]['id'].tolist()

    def get_tweet_main(self, dict_values):
        tweet_id = self.raw_data['id'].to_list()
        modal_list = ["username", "text", "place_country", "lang"]

        for key, value in dict_values.items:
            if key in modal_list:
                tweet_id = list(set(tweet_id) & set(self.get_others_tweet_id(value, key)))
            if key == "user_followers_count ":
                tweet_id = list(set(tweet_id) & set(self.get_followers_tweet_id(value)))
            if key == "timestamp":
                tweet_id = list(set(tweet_id) & set(self.get_timestamp_tweet_id(value[0], value[1])))
            if key == "hashtag":
                tweet_id = list(set(tweet_id) & set(self.get_hashtag_tweet_id(value)))

        if tweet_id == self.raw_data['id'].to_list():
            print("NO DATA...")

        return tweet_id

    def get_tweet_count(self):
        return 5