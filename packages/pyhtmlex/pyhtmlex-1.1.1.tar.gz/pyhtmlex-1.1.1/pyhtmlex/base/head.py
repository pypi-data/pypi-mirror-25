from base import *


class Head(Element):
    element_name = "head"

    def __init__(self):
        super(Head, self).__init__()


class Title(Element):
    element_name = "title"

    def __init__(self, title):
        super(Title, self).__init__()
        self.inner_html = title


class Style(Element):
    element_name = "style"

    def __init__(self):
        super(Style, self).__init__()
        self.attributes["type"] = "text/css"

    def _add(self, name, **kwargs):
        self.inner_html += "%s{" % name
        for attr, value in kwargs.items():
            if isinstance(value, int):
                value = '%dpx' % value
            self.inner_html += "%s:%s;" % (attr.replace('_', '-'), value)
        self.inner_html += "}"

    def add_tag(self, name, **kwargs):
        self._add(name, **kwargs)

    def add_id(self, name, **kwargs):
        self._add('#' + name, **kwargs)

    def add_class(self, name, **kwargs):
        self._add('.' + name, **kwargs)


class Meta(EmptyElement):
    element_name = "meta"

    def __init__(self):
        super(Meta, self).__init__()


class Link(EmptyElement):
    element_name = "link"

    def __init__(self):
        super(Link, self).__init__()


class Css(Link):
    def __init__(self, href):
        super(Css, self).__init__()
        self.attributes["rel"] = "stylesheet"
        self.attributes["type"] = "text/css"
        self.attributes["href"] = href
