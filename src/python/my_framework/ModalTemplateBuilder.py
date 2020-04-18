from my_framework.TemplateBuilder import TemplateBuilder


class ModalTemplateBuilder(TemplateBuilder):

    def __init__(self, template_path, modal_id, txt_button):
        TemplateBuilder.__init__(self, template_path)

        self.modal_id = modal_id
        self.add_pos -= 2

        self.html = self.html.replace("<insertId/>", modal_id)

        self.class_modal_pos = self.html.find("<insertClass/>")
        self.html = self.html.replace("<insertClass/>", "")

        self.html = self.html.replace("<insertTxtButton/>", txt_button)

    def insert_class(self, my_class):
        self.html = "{} {} {}".format(self.html[:self.class_modal_pos],
                                             my_class,
                                             self.html[self.class_modal_pos:])

        self.class_modal_pos += len(my_class)

    def link_to_open_model(self, txt):
        return """<a href="{}" class="js-modal">{}</a>""".format(self.modal_id, txt)

