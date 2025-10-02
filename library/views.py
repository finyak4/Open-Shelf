from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from library.utils import paginate
import json
from django.http import JsonResponse
from library import forms
from library import models
from django.utils.timezone import localtime
from django.views.decorators.csrf import csrf_exempt
from difflib import get_close_matches


def library(request):
    authors = models.Author.objects.all()
    books = models.Book.objects.all()
    genres = models.Genre.objects.all()
    form = forms.AddBook()

    if request.method == "POST":
        form = forms.AddBook(request.POST)
        if form.is_valid():
            form.save()
            return redirect("library") 
        else:
            return render(request, "library/library.html", 
                {"form": form,
                "books": books,
                "authors": authors,
                "genres": genres,
                "message": "Form is not valid. Book was not added."})
        
    query = request.GET.get('query')
    genre = request.GET.get('genre')  
    availability = request.GET.get('available')
    author = request.GET.getlist('author')
    try:
        books = models.Book.objects.filter_books(query=query, genre=genre, availability=availability, authors=author)
    except Exception as e:
        return render(request, "library/library.html", {"form": form, "books": books, "authors": authors, "message": str(e)})

    page_books, page_range, query_params = paginate(books, request)
    return render(request, "library/library.html",
        {"form": form,
        "books": page_books,
        "authors": authors,
        "genres": list(genres),
        "authors_selected": author if author else [],
        "page_range": page_range,
        "query_params": query_params,})


def book_view(request, id):
    book = get_object_or_404(models.Book, pk=id)
    genres = models.Genre.objects.all()
    if request.method == "GET":
        return render(request, "library/book_page.html", {"book": book, "genres": list(genres)})
    
    elif request.method == "PUT":
        try:
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
               
            book.save()

            return JsonResponse({"status": "success"}, status=200)

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
        
def reserve(request, id):
    if request.method == "POST":
        models.Reservation.create_reservation(id, request.user)

        return JsonResponse({"status": "success"}, status=200)
    elif request.method == "DELETE":
        try:
            models.Reservation.overdue(id)
            return JsonResponse({"status": "deleted"}, status=204)
        except models.Reservation.DoesNotExist:
            return JsonResponse({"error": "Reservation not found"}, status=404)
    return JsonResponse({"error": "Method not allowed"}, status=405)



def reservation_page(request, id):
    reservation_time = None
    reservation = None
    reservations = []
    try:
        reservation = models.Reservation.objects.get(id=id, handed=False)
        reservation_time = localtime(reservation.time).isoformat()
        reservations = models.Reservation.objects.filter(user=reservation.user, handed=False)
    except models.Reservation.DoesNotExist:
        pass
    return render(request, "library/reservation_page.html", {"reservation": reservation,"reservation_time": reservation_time, "reservations": reservations})