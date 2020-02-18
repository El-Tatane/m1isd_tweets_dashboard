ROUTES = {}


def clean_route(route):
    if route[0] != "/":
        route = "/" + route
    if route[-1] != "/":
        route += "/"
    return route


# Def decorateur router
def set_route(route):
    if route[0] != "/":
        route = "/" + route
    if route[-1] != "/":
        route += "/"

    def wrapper_set_route(func):
        assert route not in ROUTES.keys(), "REDEFINITON OF EXISTING ROUTE '{}'".format(route)
        ROUTES[route] = func
        return func
    return wrapper_set_route