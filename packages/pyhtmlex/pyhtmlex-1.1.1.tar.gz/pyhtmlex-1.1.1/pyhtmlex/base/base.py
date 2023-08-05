class Element(object):
    element_name = "null"

    def __init__(self):
        self.attributes = {}
        self.children = []
        self.inner_html = ""

        self.tag_head = ""
        self.tag_tail = ""

    def __str__(self):
        temp = "<%s" % self.element_name
        for item in self.attributes.items():
            temp += ' %s="%s"' % item
        temp += ">"
        for child in self.children:
            temp += "%s" % child
        temp += self.inner_html
        temp += "</%s>" % self.element_name
        return temp

    def generate(self):
        temp = "<%s" % self.element_name
        for item in self.attributes.items():
            temp += ' %s="%s"' % item
        temp += ">"
        yield temp
        for child in self.children:
            for item in child.generate():
                yield item
        yield self.inner_html
        yield "</%s>" % self.element_name

    def push_back(self, child):
        self.children.append(child)

    def set_attributes(self, **kwargs):
        for attr, value in kwargs.items():
            if isinstance(value, int):
                value = '%dpx' % value
            self.attributes[attr.replace('_', '-')] = value


class EmptyElement(object):
    element_name = "null"

    def __init__(self):
        self.attributes = {}

    def __str__(self):
        temp = "<%s " % self.element_name
        for item in self.attributes.items():
            temp += ' %s="%s"' % item
        temp += "\>"
        return temp

    def generate(self):
        temp = "<%s " % self.element_name
        for item in self.attributes.items():
            temp += ' %s="%s"' % item
        temp += "\>"
        yield temp

    def set_attributes(self, **kwargs):
        for attr, value in kwargs.items():
            if isinstance(value, int):
                value = '%dpx' % value
            self.attributes[attr.replace('_', '-')] = value


class Text(object):
    def __init__(self, txt):
        self.txt = txt

    def __str__(self):
        return self.txt

    def generate(self):
        yield self.txt
