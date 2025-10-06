from django.core.paginator import Paginator
import json
from difflib import get_close_matches

from django.shortcuts import render
from library import models

def paginate(queryset, request, per_page=30):
    """
    Paginate a queryset with smart page range generation.
    
    Creates a paginated result with an optimized page range display that shows:
    - First few pages when near start
    - Last few pages when near end  
    - Pages around current page when in middle
    - Ellipsis (...) for skipped page ranges
    
    Args:
        queryset: Django queryset to paginate
        request: HttpRequest object for getting page parameter
        per_page: Number of items per page (default: 30)
    
    Returns:
        tuple: (page_objects, page_range, query_string)
            - page_objects: Page object from Paginator
            - page_range: List of page numbers with ellipsis for UI
            - query_string: URL-encoded query parameters without 'page'
    """
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

def render_library_page(request, form, books, authors, genres, message=None, authors_selected=None):
    """
    Render the library page with paginated books and filter context.
    
    Prepares all necessary context data for the library template including
    paginated books, filter forms, and optional status messages.
    
    Args:
        request: HttpRequest object
        form: Book Addition form instance
        books: Queryset of books to display
        authors: Queryset of all authors for filter
        genres: Queryset of all genres for filter
        message: Optional status message to display (e.g., success/error)
        authors_selected: Optional list of selected author IDs for filter persistence
    
    Returns:
        HttpResponse: Rendered library template with context
    """
    page_books, page_range, query_params = paginate(books, request)
    context = {
        "form": form,
        "books": page_books,
        "authors": authors,
        "genres": list(genres),
        "page_range": page_range,
        "query_params": query_params,
    }
    if message:
        context["message"] = message
    if authors_selected:
        context["authors_selected"] = authors_selected
    return render(request, "library/library.html", context)

def edit_book(request, book):
    """
    Update book details from JSON data with author/genre handling.

    Handles creation of new authors and genres using fuzzy matching to prevent
    duplicates. Validates data before saving.
    """
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
    """
    Create a new book with author and genre handling.
    
    Processes a validated book form by creating or finding matching
    author and genre objects before saving the book. Uses fuzzy
    matching to prevent duplicate authors/genres.
    
    Args:
        form: Validated AddBook form instance
        request: HttpRequest for context
    
    Returns:
        Book: The newly created book instance
    
    Process:
        1. Extracts author and genre names from form data
        2. Uses fuzzy matching to find existing authors/genres
        3. Creates new authors/genres if no close match found
        4. Assigns objects to book and saves
    
    Note:
        Should be called within a database transaction to ensure
        data consistency if used in a view with transaction.atomic()
    """
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