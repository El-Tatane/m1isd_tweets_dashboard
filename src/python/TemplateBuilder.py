import os

class TemplateBuilder:

    def __init__(self, template_path):
        self.template_path = template_path
        with open(os.path.join("src/ressources/templates/", self.template_path), "r") as f:
            self.html = f.read()
        self.add_pos = self.html.find("<insert/>")
        self.html = self.html.replace("<insert/>", "")

    def get_html(self):
        return self.html

    def insert_element(self, type_elemet, inner_html):
        self.html = "{}<{}>{}</{}>{}".format(self.html[:self.add_pos],
                                               type_elemet,
                                               inner_html,
                                               type_elemet,
                                               self.html[self.add_pos:])

        self.add_pos += 5 + 2 * len(type_elemet) + len(inner_html)