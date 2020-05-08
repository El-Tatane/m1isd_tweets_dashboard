from .Singleton import Singleton

class Cache(metaclass=Singleton):

    def __init__(self, size):
        self.size = size
        self.data = {}
        self.order = [None] * size
        self.pos = 0

    def add_element(self, dict_param, data):
        self.data.pop(self.order[self.pos], None)
        key = hash(str(dict_param))
        self.order[self.pos] = key
        self.data[key] = data
        self.pos = (self.pos + 1) % self.size

    def get_cache(self, dict_param):
        key = hash(str(dict_param))
        if key in self.order:
            return self.data[key]
        return None

    def pp(self):
        print(self.data)
        print(self.order)


if __name__ == "__main__":
    t = Cache(2)
    print(t.get_cache("a"))
    t.add_element("a", 1)
    t.add_element("b", 2)
    t.pp()
    print(t.get_cache("a"))
    print(t.get_cache("b"))

    t.add_element("c", 3)
    t.pp()
    print(t.get_cache("a"))
    print(t.get_cache("b"))
    print(t.get_cache("c"))

    z = Cache(3)

    print(t,z)