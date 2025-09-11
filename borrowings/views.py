from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
import json
from .models import Borrowing
from library.models import Reservation
from library.models import Book
from home.models import User
# Create your views here.

def borrowings(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        try:
            book_id = int(data.get("id"))
        except KeyError:
            book_id = None 
        if book_id:
            Borrowing.return_book(book_id)
        return JsonResponse({"status": "success"}, status=200)
    else:
        user_reservations = Reservation.objects.filter(user=request.user, handed=False)
        reservations = Reservation.objects.filter(handed=False)
        user_borrowings = Borrowing.objects.filter(user=request.user, return_date=None)
        borrowings = Borrowing.objects.filter(return_date=None)
        return render (request, "borrowings/borrowings.html", {"user_reservations": user_reservations, "reservations": reservations, "user_borrowings": user_borrowings, "borrowings": borrowings})


def borrow(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        user = User.objects.get(id=user_id)
        reservation_ids = request.POST.getlist("reservation_id")
        reservation_ids = list(map(int, reservation_ids))

        reservations = Reservation.objects.filter(id__in=reservation_ids, user=user_id, handed=False)

        book_ids = reservations.values_list("book_id", flat=True)
        books = Book.objects.filter(id__in=book_ids)

        Borrowing.create(user=user, books=books)

        for reservation in reservations:
            reservation.hand_book(reservation.id)

    return redirect("borrowings")


def borrow_man(request):
    if request.method == "POST":
        data = json.loads(request.body)
        
        username = data.get('user')
        book_ids = list(data.get('books'))

        books = Book.objects.filter(id__in=book_ids)
        user = User.objects.get(username=username)


        borrowing = Borrowing.create(user=user, books=books)
        for book in books:
            book.availability -= 1
            book.save()
        return JsonResponse({"status": "success"}, status=200)

def autocomplete(request):
    q = request.GET.get('q', '')
    if q:
        results = User.objects.filter(username__icontains=q)[:10]
        suggestions = [{'username': user.username} for user in results]
    else:
        suggestions = []
    return JsonResponse(suggestions, safe=False)

def autocomplete_books(request):
    q = request.GET.get('q', '')
    if q:
        results = Book.objects.filter(id__icontains=q)[:10]
        suggestions = [{'id': b.id, 'title': b.title} for b in results]
    else:
        suggestions = []
    return JsonResponse(suggestions, safe=False)