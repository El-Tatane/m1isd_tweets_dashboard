import socketserver
import pandas as pd
from src.python.my_framework.Request import Request
from DataLoader import DataLoader
from routes import ROUTES
import re
import io

PORT = 80
data_filepath = "D:/Users/zakar/Documents/Mes_Documents_2019_2020/ISD/langages_dynamiques/KN/projetJavaScript" \
                "/m1isd_tweets_dashboard/tweets.csv "

if __name__ == "__main__":
    # print("start")
    # my_request = Request

    # my_server = socketserver.TCPServer(("", PORT), my_request)

    # Star the server
    #  my_server.serve_forever()
    # my_request.parse_arg()

    tweet_data = DataLoader(data_filepath)

