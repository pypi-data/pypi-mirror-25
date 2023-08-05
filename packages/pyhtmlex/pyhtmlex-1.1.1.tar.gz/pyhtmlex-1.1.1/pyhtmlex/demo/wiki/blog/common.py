# -*- coding: UTF-8 -*-
from wiki.body import *
import os


class BlogList(object):
    blog_list = {}
    blog_list_ul = {}

    @classmethod
    def generate_list(cls, category):
        ret = {'dir': {}, 'file': {}}
        pathname = settings.BLOG_DIR + category
        for parent, dirnames, filenames in os.walk(pathname):
            for dirname in dirnames:
                if dirname in ['img', 'code']:
                    continue
                url = '/blog/%s/%s/' % (category, dirname)
                ret['dir'][url] = (parent, dirname.decode('GBK'))  # dir.decode('GBK')

            for title in filenames:
                url = '/blog/%s/%s' % (category, title)
                ret['file'][url] = (parent, title[:-4].decode('GBK'))
            break
        cls.blog_list[category] = ret
        return ret

    @classmethod
    def get_list(cls, category):
        category_list = cls.generate_list(category)
        ts = ['dir', 'file']
        all_ls = []
        for t in ts:
            content = category_list[t]
            if not content:
                continue

            ls = Ul()
            if t == 'file':
                ls.set_attributes(style='list-style: none; padding-left: 20px;')
            for key, value in content.items():
                li = Li()
                li.push_back(A(key, value[1]))
                ls.push_back(li)
            all_ls.append(ls)

        return all_ls

    @classmethod
    def get(cls, category):
        ls = cls.blog_list_ul.get(category)
        if ls is None:
            ls = cls.get_list(category)
            cls.blog_list_ul[category] = ls
        return ls


def _mk_bread(category, title=None):
    bread = [("/", "首页"),]
    temp = category
    while temp:
        aa, bb, cc = temp.rpartition('/')
        bread.insert(1, ("/blog/%s/" % temp, cc))
        temp = aa
    if title is not None:
        bread.append(("/blog/%s/%s" % (category, id), title))
    return bread


def blog_list_body(category):
    bread = _mk_bread(category)

    body, style, left, right = body_factory(bread)

    for ls in BlogList.get(category):
        right.push_back(ls)

    return body, style


def blog_page_body(category, id):
    file_list = BlogList.get(category)
    url = '/blog/%s/%s' % (category, id)
    pathname, title = BlogList.blog_list[category]['file'][url]

    bread = _mk_bread(category, title)

    body, style, left, right = body_factory(bread)

    for ls in file_list:
        left.push_back(ls)

    right_style = md_parser(right, pathname, title)

    style.extend(right_style)

    return body, style
