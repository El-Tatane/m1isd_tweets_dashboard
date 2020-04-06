import os


class TemplateBuilder:
    def __init__(self, template_path):
        self.template_path = template_path

        with open(os.path.join("../ressources/templates/", self.template_path), "r") as f:
            self.html = f.read()

        self.add_pos = self.html.find("<insert/>")
        self.html = self.html.replace("<insert/>", "")

    def get_html(self):
        return self.html

    def insert_simple_element(self, type_elemet):
        self.html = "{}<{}/>{}".format(self.html[:self.add_pos],
                                               type_elemet,
                                               self.html[self.add_pos:])

        self.add_pos += 3 + len(type_elemet)

    def insert_double_element(self, type_elemet, inner_html):
        self.html = "{}<{}>{}</{}>{}".format(self.html[:self.add_pos],
                                               type_elemet,
                                               inner_html,
                                               type_elemet,
                                               self.html[self.add_pos:])

        self.add_pos += 5 + 2 * len(type_elemet) + len(inner_html)

    def insert_raw_html(self, raw_html):
        self.html = "{}{}{}".format(self.html[:self.add_pos],
                                             raw_html,
                                             self.html[self.add_pos:])

        self.add_pos += len(raw_html)