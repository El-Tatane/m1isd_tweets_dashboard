import socketserver
import pandas as pd
from src.python.my_framework.Request import Request
from DataLoader import DataLoader
from routes import ROUTES

PORT = 80
data_filepath = ""

if __name__ == "__main__":
     print("start")
     my_request = Request

     my_server = socketserver.TCPServer(("", PORT), my_request)

    # Star the server
     my_server.serve_forever()
    # my_request.parse_arg()
    #data = DataLoader(data_filepath)
    #print(data.get_hashtag_tweet_id('airforce1'))
    #print(data.get_tweet_id(4918871526, 'user_id'))
    #print(data.get_tweet_id('jatno', 'user_name'))

    #print(data.get_tweet_latitude(1080002946824318976))
    #print(data.get_tweet_longitude(1080002946824318976))
    #print(data.get_user_id_most_or_least_follow(most=False))
    #print(data.get_user_id_least_follow())
    #print(data.get_user_id_follow_per_country(min_c = True))
    #print(data.get_user_id_most_or_least_follow_in_country())
