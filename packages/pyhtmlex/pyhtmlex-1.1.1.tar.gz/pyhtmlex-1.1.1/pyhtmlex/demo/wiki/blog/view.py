from django.http import StreamingHttpResponse
from common import *
from pyhtmlex.base.root import *


def main(request):
    path = request.path[5:]
    category, _, name = path.rpartition('/')
    category = category.strip('/')

    if not name:
        body, styles = blog_list_body(category)
        head = lazy_head(category, styles)
        response = StreamingHttpResponse(Html(head, body).generate())

        return response

    body, styles = blog_page_body(category, name)
    head = lazy_head(category + name, styles)
    response = StreamingHttpResponse(Html(head, body).generate())

    return response
