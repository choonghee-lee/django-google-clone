from django.shortcuts import render


def index_page(request):
    return render(
        request,
        'index.html'
    )


def search_page(request):
    term = request.GET.get('term', 'google')
    searchType = request.GET.get('type', 'sites')
    return render(
        request,
        'search.html',
        {
            'term': term,
            'type': searchType,
        }
    )
