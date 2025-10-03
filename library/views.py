from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from library.utils import paginate, edit_book
from django.http import JsonResponse
from library import forms
from library import models
from django.views.decorators.csrf import csrf_exempt


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
            edit_book(request, book)
            return JsonResponse({"status": "success"}, status=200)

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
        
# def reserve(request, id):
#     if request.method == "POST":
#         models.Reservation.create_reservation(id, request.user)

#         return JsonResponse({"status": "success"}, status=200)
#     elif request.method == "DELETE":
#         try:
#             models.Reservation.overdue(id)
#             return JsonResponse({"status": "deleted"}, status=204)
#         except models.Reservation.DoesNotExist:
#             return JsonResponse({"error": "Reservation not found"}, status=404)
#     return JsonResponse({"error": "Method not allowed"}, status=405)



# def reservation_page(request, id):
#     reservation_time = None
#     reservation = None
#     reservations = []
#     try:
#         reservation = models.Reservation.objects.get(id=id, handed=False)
#         reservation_time = localtime(reservation.time).isoformat()
#         reservations = models.Reservation.objects.filter(user=reservation.user, handed=False)
#     except models.Reservation.DoesNotExist:
#         pass
#     return render(request, "library/reservation_page.html", {"reservation": reservation,"reservation_time": reservation_time, "reservations": reservations})