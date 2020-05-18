from my_framework.Request import Request, ThreadedRequest
from DataLoader import DataLoader

# Read config
from initialization import DICT_CONFIG


if __name__ == "__main__":

    # Load data
    data_loader = DataLoader(DICT_CONFIG["list_file_path"])
    print("data raw size", data_loader.df_raw_data.shape)

    # Register all routes in the http server
    from routes import *

    # Create HTTP sever with Thread
    my_server = ThreadedRequest(("", DICT_CONFIG["port"]), Request)
    # Star the server
    my_server.serve_forever()
