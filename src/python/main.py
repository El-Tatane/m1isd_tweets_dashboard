import socketserver
from my_framework.Request import Request
from DataLoader import DataLoader
from routes import ROUTES
from yaml import safe_load
import os

PORT = 80
data_filepath = ""

if __name__ == "__main__":

    # configuration file
    this_dir = os.path.dirname(__file__)
    with open(os.path.join(this_dir, "../..", "config.yml"), 'r') as stream:
        DICT_CONFIG = safe_load(stream)

    # Load data
    data_loader = DataLoader(DICT_CONFIG["list_file_path"])

    # my_request = Request
    # my_server = socketserver.TCPServer(("", PORT), my_request)
    #
    # # Star the server
    # my_server.serve_forever()

    print("-------")
    print(data_loader.filter_tweets({"timestamp": [1546327972665, 1546327972667]}))
