# -*- coding: UTF-8 -*-
from django.http import StreamingHttpResponse
from pyhtmlex.base.root import *
from body import *


def body_main():
    body, style, left, right = body_factory([("/", "首页")])

    right_style = md_parser(right, os.path.join(os.path.dirname(__file__)), 'readme')
    style.extend(right_style)

    return body, style


def main(request):
    body, styles = body_main()
    head = lazy_head("my PyHtmlEx", styles)
    response = StreamingHttpResponse(Html(head, body).generate())

    return response
