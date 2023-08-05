# -*- coding: UTF-8 -*-
import os
import sys
file_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(file_path, ".."))

from base.root import *
from wiki.wiki.body import *


def body_main(content):
    body, style, left, right = body_factory([("/", "首页")])

    right.push_back(content)

    style.append(content.style)
    return body, style


def code():
    with open("remote_shell.py", 'r') as f:
        lines = f.readlines()

    body, styles = body_main(PythonCode(lines))
    head = lazy_head("code", styles)

    with open('code.html', 'w') as f:
        f.write('%s' % Html(head, body))


def console():
    with open("remote_shell.py", 'r') as f:
        lines = f.readlines()

    body, styles = body_main(Console(lines))
    head = lazy_head("console", styles)

    with open('console.html', 'w') as f:
        f.write('%s' % Html(head, body))


if __name__ == '__main__':
    code()
    console()
