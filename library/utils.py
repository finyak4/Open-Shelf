from django.core.paginator import Paginator

def paginate(queryset, request, per_page=30):
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get('page')
    page_books = paginator.get_page(page_number)

    current_page = page_books.number
    total_pages = paginator.num_pages
    page_range = []

    query_params = request.GET.copy()
    if 'page' in query_params:
        query_params.pop('page')

    if total_pages <= 10:
        page_range = range(1, total_pages + 1)
    else:
        if current_page <= 5:
            page_range = list(range(1, 8)) + ["..."] + [total_pages]
        elif current_page >= total_pages - 5:
            page_range = [1] + ["..."] + list(range(total_pages - 6, total_pages + 1))
        else:
            page_range = [1] + list(range(current_page - 3, current_page + 3)) + ["..."] + [total_pages]
    return page_books, page_range, query_params.urlencode()
