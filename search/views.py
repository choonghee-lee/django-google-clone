from django.shortcuts import render


def index_page(request):
    return render(
        request,
        'search/index.html'
    )


def search_page(request):
    term = request.GET.get('term', 'google')
    return render(
        request,
        'search/search.html',
        {'term': term}
    )
