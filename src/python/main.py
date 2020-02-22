import socketserver

from src.python.my_framework.Request import Request
from src.python.DataLoader import DataLoader
from src.python.routes import ROUTES

PORT = 80
data_filepath = "tweets.csv"

if __name__ == "__main__":
    print("start")
    my_request = Request

    my_server = socketserver.TCPServer(("", PORT), my_request)

    # Star the server
    my_server.serve_forever()

    # data = DataLoader(data_filepath)