from django.shortcuts import render
from .parser import (
    DomDocumentParser,
    create_link,
    refine_links,
)


def index_page(request):
    return render(
        request,
        'index.html'
    )


def search_page(request):
    term = request.GET.get('term', 'google')
    searchType = request.GET.get('type', 'sites')

    url = "http://www.bbc.com"
    parser = DomDocumentParser()
    links = parser.get_links(url)
    refined_links = refine_links(url, links)

    return render(
        request,
        'search.html',
        {
            'term': term,
            'type': searchType,
            'links': refined_links
        }
    )
