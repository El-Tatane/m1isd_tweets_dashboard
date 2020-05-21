from my_framework.Request import Request, ThreadedRequest
from DataLoader import DataLoader

# Read config
from initialization import DICT_CONFIG


if __name__ == "__main__":

    # Load data
    data_loader = DataLoader(data_path=DICT_CONFIG["data_path"],
                             list_filename=DICT_CONFIG["list_filename"],
                             size_cache=DICT_CONFIG["cache_size"])

    # Register all routes in the http server
    from routes import *

    # Create HTTP sever with Thread
    my_server = ThreadedRequest(("", DICT_CONFIG["port"]), Request)
    # Star the server
    my_server.serve_forever()
