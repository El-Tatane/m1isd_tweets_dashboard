import socketserver

from MyRequest import MyRequest
from Data import Data
from routes import ROUTES

PORT = 80
filepath = "tweets.csv"

if __name__ == "__main__":
    print("start")
    my_request = MyRequest

    my_server = socketserver.TCPServer(("", PORT), my_request)

    # Star the server
    my_server.serve_forever()

    # data = Data(filepath)