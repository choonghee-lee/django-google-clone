from django.shortcuts import render
from .parser import (
    DomDocumentParser,
    create_link,
    refine_links,
)
from .models import Site, Image


def index_page(request):
    return render(
        request,
        'index.html'
    )


def search_page(request):
    term = request.GET.get('term', 'google')
    searchType = request.GET.get('type', 'sites')

    # url = "http://www.bbc.com"
    # parser = DomDocumentParser()
    # links = parser.get_links(url)
    # refined_links = refine_links(url, links)

    links = Site.objects.filter(title__contains=term) | Site.objects.filter(
        url__contains=term) | Site.objects.filter(description__contains=term) | Site.objects.filter(keywords__contains=term)
    links = links.order_by('-clicks')
    links_count = links.count()

    return render(
        request,
        'search.html',
        {
            'term': term,
            'type': searchType,
            'links': links,
            'links_count': links_count,
        }
    )
