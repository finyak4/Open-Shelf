from django.core.paginator import Paginator
import json
from difflib import get_close_matches
from library import models

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

def edit_book(request, book):
    data = json.loads(request.body)

    book.title = data.get("title", book.title)
    book.description = data.get("description", book.description)
    book.availability = data.get("availability", book.availability)
    book.publication_year = data.get("year", book.publication_year)
    book.cover_image = data.get("url", book.cover_image)
            
    author_name = data.get("author", "").strip()
    if author_name:
        existing_authors = list(models.Author.objects.values_list('name', flat=True))
        close_matches = get_close_matches(author_name, existing_authors, n=1, cutoff=0.8)
        if close_matches:
            author_obj = models.Author.objects.get(name=close_matches[0])
        else:
            author_obj = models.Author.objects.create(name=author_name)
        book.author = author_obj

    genre_name = data.get("genre", "").strip()
    if genre_name:
        existing_genres = list(models.Genre.objects.values_list('name', flat=True))
        close_matches = get_close_matches(genre_name, existing_genres, n=1, cutoff=0.8)
        if close_matches:
            genre_obj = models.Genre.objects.get(name=close_matches[0])
        else:
            genre_obj = models.Genre.objects.create(name=genre_name)
        book.genre = genre_obj
        
    book.full_clean()
    book.save()

def add_book_creation(form, request):
    author_name = form.cleaned_data['author'].strip()
    genre_name = form.cleaned_data['genre'].strip()

    # Handle Author
    existing_authors = list(models.Author.objects.values_list('name', flat=True))
    close_matches = get_close_matches(author_name, existing_authors, n=1, cutoff=0.8)
    if close_matches:
        author_obj = models.Author.objects.get(name=close_matches[0])
    else:
        author_obj = models.Author.objects.create(name=author_name)

    # Handle Genre
    existing_genres = list(models.Genre.objects.values_list('name', flat=True))
    close_matches = get_close_matches(genre_name, existing_genres, n=1, cutoff=0.8)
    if close_matches:
        genre_obj = models.Genre.objects.get(name=close_matches[0])
    else:
        genre_obj = models.Genre.objects.create(name=genre_name)

    book = form.save(commit=False)  
    book.author = author_obj  
    book.genre = genre_obj  
    book.save()  
    return book