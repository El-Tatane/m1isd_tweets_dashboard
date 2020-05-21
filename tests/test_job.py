from DataLoader import *
from pandas.util.testing import assert_frame_equal
import pandas as pd

dataloader = DataLoader()


def test_filter_text_equal_tweets():
    column_df = pd.DataFrame({'user_name': ['Zak', 'Antoine', None, 'Tatan'], \
                              'place_country': ['France', None, 'Us', 'China'], \
                              'lang': [None, 'fr', 'dz', 'en']})

    result_df_user_name = pd.DataFrame({'user_name': ['Zak', 'Antoine'], \
                                        'place_country': ['France', None], \
                                        'lang': [None, 'fr']})

    result_df_place_country = pd.DataFrame({'user_name': ['Tatan'], \
                                            'place_country': ['China'], \
                                            'lang': ['en']})

    result_df_lang = pd.DataFrame({'user_name': [None], \
                                   'place_country': ['Us'], \
                                   'lang': ['dz']})

    assert_frame_equal(
        dataloader.filter_text_equal_tweets(column_df, 'user_name', ['Zak', 'Antoine']).reset_index(drop=True), \
        result_df_user_name.reset_index(drop=True))

    assert_frame_equal(
        dataloader.filter_text_equal_tweets(column_df, 'place_country', ['China']).reset_index(drop=True), \
        result_df_place_country.reset_index(drop=True))

    assert_frame_equal(dataloader.filter_text_equal_tweets(column_df, 'lang', ['dz']).reset_index(drop=True), \
                       result_df_lang.reset_index(drop=True))


def test_filter_text_contain_tweets():
    text_contain_df = pd.DataFrame({'user_name': ['Zak', 'Antoine', None, 'Zak'], \
                                    'text': ['Hello world', 'lovely cat', 'goool Ronaldo did it', '']})

    result_df = pd.DataFrame({'user_name': ['Antoine', None], \
                              'text': ['lovely cat', 'goool Ronaldo did it']})

    assert_frame_equal(
        dataloader.filter_text_contain_tweets(text_contain_df, 'text', ['cat', 'Ronaldo']).reset_index(drop=True), \
        result_df.reset_index(drop=True))


def test_filter_hashtage_tweets():
    hashtag_df = pd.DataFrame({'hashtag_0': ['foot', 'love', 'trump'], \
                               'hashtag_1': ['plage', None, 'soleil'], \
                               'hashtag_2': ['nada', None, None]})

    result_df = pd.DataFrame({'hashtag_0': ['love'], \
                              'hashtag_1': [None], \
                              'hashtag_2': [None]})
    assert_frame_equal(dataloader.filter_hashtag_tweets(hashtag_df, ['love']).reset_index(drop=True), result_df \
                       .reset_index(drop=True))


def test_filter_user_followers_count_tweets():
    followers_count_df = pd.DataFrame({'user_followers_count': [15.0, 20.0, 30.0, 0.0, None]})
    result_df = pd.DataFrame({'user_followers_count': [20.0, 30.0]})
    assert_frame_equal(dataloader.filter_user_followers_count_tweets(followers_count_df, 20).reset_index(drop=True), \
                       result_df.reset_index(drop=True))


def test_filter_timestamp_tweets():
    timestamp_df = pd.DataFrame({'timestamp': [1.2e9, 1.3e9, 1.4e9, 1.5e9, None]})
    result_df_min_max = pd.DataFrame({'timestamp': [1.3e9, 1.4e9]})
    result_df_min = pd.DataFrame({'timestamp': [1.3e9, 1.4e9, 1.5e9]})
    result_df_max = pd.DataFrame({'timestamp': [1.2e9, 1.3e9, 1.4e9]})
    assert_frame_equal(dataloader.filter_timestamp_tweets(timestamp_df, 1.3e9, 1.4e9).reset_index(drop=True), \
                       result_df_min_max.reset_index(drop=True))
    assert_frame_equal(dataloader.filter_timestamp_tweets(timestamp_df, ts_min=1.3e9).reset_index(drop=True), \
                       result_df_min.reset_index(drop=True))
    assert_frame_equal(dataloader.filter_timestamp_tweets(timestamp_df, ts_max=1.4e9).reset_index(drop=True), \
                       result_df_max.reset_index(drop=True))


if __name__ == "__main__":
    test_filter_hashtage_tweets()
    test_filter_user_followers_count_tweets()
    test_filter_timestamp_tweets()
    test_filter_text_equal_tweets()
    test_filter_text_contain_tweets()
