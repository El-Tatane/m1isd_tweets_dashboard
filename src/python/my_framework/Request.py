import http.server
import warnings

from src.python.my_framework.router import ROUTES, clean_route


class Request(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):

        # Sending an '200 OK' response
        self.send_response(200)

        # Setting the header
        self.send_header("Content-type", "text/html")

        # Whenever using 'send_header', you also have to call 'end_headers'
        self.end_headers()

        # Extract query param
        route, args = self.parse_arg(self.path)
        print(args)

        if route is None or route not in ROUTES.keys():
            route = "error_404"

        html = ROUTES[clean_route(route)]()
        print(html)

        # Writing the HTML contents with UTF-8
        self.wfile.write(bytes(html, "utf8"))

        return

    @staticmethod
    def parse_arg(string):
        route, args = None, None

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
            return args
        except (LookupError, ValueError) as e:
            warnings.warn("Incorrect URL '{}".format(string))
            return None, None

