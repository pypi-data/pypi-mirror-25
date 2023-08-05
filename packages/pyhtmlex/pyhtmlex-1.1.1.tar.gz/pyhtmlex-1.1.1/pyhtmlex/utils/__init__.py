# -*- coding: UTF-8 -*-
from table import *
from md_parser import *


def lazy_head(title, styles):
    head = Head()
    meta = Meta()
    meta.set_attributes(http_equiv="Content-Type", content="text/html; charset=utf-8")
    head.push_back(meta)
    # head.push_back(Css("static/css/test.css"))
    for style in styles:
        head.push_back(style)
    head.push_back(Title(title))
    return head


class Logo(Div):
    def __init__(self, cls_name, pic_path, link):
        super(Logo, self).__init__(cls_name)
        a = A(link)
        a.push_back(Img(pic_path))
        self.children.append(a)


class Navigate(Div):
    def __init__(self, cls_name, sub_cls_name, name_links):
        super(Navigate, self).__init__(cls_name)
        for name_link in name_links:
            div = Div(sub_cls_name)
            a = A(*name_link)
            div.push_back(a)
            self.children.append(div)


class Breadcrumbs(Div):
    def __init__(self, cls_name, name_links):
        super(Breadcrumbs, self).__init__(cls_name)
        for name_link in name_links:
            a = A(*name_link)
            self.children.append(a)
            txt = Text(">>")
            self.children.append(txt)
        self.children.pop()
