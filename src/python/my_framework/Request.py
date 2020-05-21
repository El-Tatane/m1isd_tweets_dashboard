from http.server import HTTPServer, BaseHTTPRequestHandler
import warnings, os
from socketserver import ThreadingMixIn

from my_framework.router import ROUTES, clean_route


class Request(BaseHTTPRequestHandler):

    def do_GET(self):

        # Sending an '200 OK' response
        self.send_response(200)

        sendReply = False
        if self.path.endswith(".js"):
            # delete first / because os.path.join didn't work later :
            # https://stackoverflow.com/questions/1945920/why-doesnt-os-path-join-work-in-this-case
            self.path = self.path[1:]
            mimetype = 'application/javascript'
            sendReply = True

        if self.path.endswith(".css"):
            # Same idea
            self.path = self.path[1:]
            mimetype = 'text/css'
            sendReply = True


        if sendReply == True:
            # Open the static file requested and send it
            this_dir = os.path.dirname(__file__)
            f = open(os.path.join(this_dir, "..", "..", self.path))
            self.send_response(200)
            self.send_header('Content-type', mimetype)
            self.end_headers()
            self.wfile.write(bytes(str(f.read()), "utf8"))
            f.close()
            sendReply = False
            return

        # Setting the header
        self.send_header("Content-type", "text/html")

        # Whenever using 'send_header', you also have to call 'end_headers'
        self.end_headers()

        # Extract query param
        route, args = self.parse_arg(self.path)
        route = clean_route(route)
        if route is None or route not in ROUTES.keys():
            route = "/error_404/"

        html = ROUTES[route](**args)

        # Writing the HTML contents with UTF-8
        self.wfile.write(bytes(str(html), "utf8"))

        return

    @staticmethod
    def parse_arg(string):
        route, args = None, {}

        separator = string.find("?")

        if separator == -1:
            return string, args

        route = string[:separator]
        str_args = string[separator + 1:]
        args = {}

        try:
            if str_args.find("&") == -1:
                key, value = str_args.split("=")
                return route, {key: value}

            for str_arg in str_args.split('&'):
                key, value = str_arg.split("=")
                args[key] = value
            return route, args
        except (LookupError, ValueError) as e:
            warnings.warn("Incorrect URL '{}".format(string))
            return None, {}


class ThreadedRequest(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""