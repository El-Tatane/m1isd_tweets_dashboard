import socketserver
from my_framework.Request import Request
from DataLoader import DataLoader

# Read config
from initialization import DICT_CONFIG



if __name__ == "__main__":

    # Load data
    data_loader = DataLoader(DICT_CONFIG["list_file_path"])
    print("data raw size", data_loader.df_raw_data.shape)

    # Register all routes in the http server
    from routes import *

    # Create HTTP sever
    my_request = Request
    my_server = socketserver.TCPServer(("", DICT_CONFIG["port"]), my_request)

    # Star the server
    my_server.serve_forever()




    # df = data_loader.filter_tweets({"text": ["Mau"], "timestamp": {"ts_start": None, "ts_end": None}})
    #
    # print(df["user_id"])

    # import threading
    #
    #
    # daemon = threading.Thread(name='daemon_server',
    #                           target=my_server.serve_forever(),  )
    # daemon.setDaemon(True) # Set as a daemon so it will be killed once the main thread is dead.
    # daemon.start()