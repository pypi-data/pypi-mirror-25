from base import *


class Body(Element):
    element_name = "body"

    def __init__(self):
        super(Body, self).__init__()


class Div(Element):
    element_name = "div"

    def __init__(self, cls_name=None):
        super(Div, self).__init__()
        if cls_name:
            self.attributes["class"] = cls_name


class Span(Element):
    element_name = "span"

    def __init__(self, txt, cls_name=None):
        super(Span, self).__init__()
        self.inner_html = txt
        if cls_name:
            self.attributes["class"] = cls_name


class Pre(Element):
    element_name = "pre"

    def __init__(self, txt=None):
        super(Pre, self).__init__()
        if txt is not None:
            self.inner_html = txt


class H(Element):
    element_name = "h"

    def __init__(self, txt, i=1):
        super(H, self).__init__()
        if i == 1:
            self.attributes["align"] = "center"
        self.element_name += "%s" % i
        self.inner_html = txt


class P(Element):
    element_name = "p"

    def __init__(self, txt):
        super(P, self).__init__()
        self.inner_html = txt


class A(Element):
    element_name = "a"

    def __init__(self, href, txt="", blank=False):
        super(A, self).__init__()
        self.attributes["href"] = href
        if blank:
            self.attributes["target"] = "_blank"
        self.inner_html = txt


class Img(EmptyElement):
    element_name = "img"

    def __init__(self, src):
        super(Img, self).__init__()
        self.attributes["src"] = src


class Table(Element):
    element_name = "table"

    def __init__(self, cls_name=None):
        super(Table, self).__init__()
        if cls_name:
            self.attributes["class"] = cls_name


class Tr(Element):
    element_name = "tr"

    def __init__(self, cls_name=None):
        super(Tr, self).__init__()
        if cls_name:
            self.attributes["class"] = cls_name

    def combine_col(self, beg, end):
        self.children[beg].attributes.pop('width')
        self.children[beg].set_attributes(colspan="%s" % (end - beg + 1))
        for i in range(beg + 1, end + 1):
            self.children.pop(beg + 1)


class Th(Element):
    element_name = "th"

    def __init__(self, width):
        super(Th, self).__init__()
        self.attributes["width"] = '%spx' % width


class Td(Element):
    element_name = "td"

    def __init__(self, width):
        super(Td, self).__init__()
        self.attributes["width"] = '%spx' % width


class Ul(Element):
    element_name = "ul"

    def __init__(self):
        super(Ul, self).__init__()


class Ol(Element):
    element_name = "ol"

    def __init__(self):
        super(Ol, self).__init__()


class Li(Element):
    element_name = "li"

    def __init__(self, txt=None, cls_name=None):
        super(Li, self).__init__()
        if txt is not None:
            self.inner_html = txt
        if cls_name is not None:
            self.attributes["class"] = cls_name


class Script(Element):
    element_name = "script"

    def __init__(self, txt):
        super(Script, self).__init__()
        self.inner_html = txt
