from base import *


class Html(Element):
    element_name = "html"

    def __init__(self, head, body):
        super(Html, self).__init__()
        self.children = [head, body]
