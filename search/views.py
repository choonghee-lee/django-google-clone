from django.shortcuts import render
from .parser import (
    DomDocumentParser,
    create_link,
    crawl_links,
)
from .models import Site, Image


def index_page(request):
    """
    인덱스 페이지 
    """
    return render(
        request,
        'index.html'
    )


def search_page(request):
    """
    검색 페이지

    검색어를 통해 데이터베이스에 있는 웹사이트 또는 이미지 정보를 리턴
    """
    term = request.GET.get('term', 'google')
    searchType = request.GET.get('type', 'sites')

    # 웹사이트 파싱
    # url = "http://www.bbc.com"
    # parser = DomDocumentParser()
    # links = parser.get_links(url)
    # refined_links = crawl_links(url, links)

    # DB에서 웹사이트 정보 꺼내오기
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
