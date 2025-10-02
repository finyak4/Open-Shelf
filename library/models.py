from django.db import models
from home.models import User
from library.validators import validate_four_digits
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db.models import Q

class Genre(models.Model):
    name = models.CharField(max_length=64, unique=True)

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"
        db_table = "genres"

    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.CharField(max_length=1024, blank=True, null=True)

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"
        db_table = "authors"

    def __str__(self):
        return self.name    

class BookManager(models.Manager):
    def filter_books(self, query=None, genre=None, availability=None, authors=None):
        books = self.all()
        if query:
            books = books.filter(Q(title__icontains=query) | Q(author__name__icontains=query))
        if genre:
            books = books.filter(genre__name__icontains=genre)
        if availability:
            if availability == "true":
                books = books.filter(availability__gt=0)
            elif availability == "false":
                books = books.filter(availability__lt=1)
        if authors:
            books = books.filter(author__name__in=authors)
        return books

class Book(models.Model):    
    title = models.CharField(max_length=128)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, max_length=128, related_name="books", null=True)
    description = models.CharField(validators=[MinLengthValidator(128), MaxLengthValidator(1024)])
    availability = models.PositiveIntegerField(default=0)
    publication_year = models.PositiveIntegerField(validators=[validate_four_digits])
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, related_name="books")
    cover_image = models.URLField ()

    objects = BookManager()

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"
        db_table = "books"    

class Reservation(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    handed = models.BooleanField(default=False)
    overdued = models.BooleanField(default=False)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Reservation"
        verbose_name_plural = "Reservations"
        db_table = "reservations"

    @staticmethod
    def create_reservation(book_id, user):
        book = Book.objects.get(id = book_id)

        if book.availability <= 0:
            raise ValueError("Book is not available for reservation.")
        
        reservation = Reservation(book = book, user = user)
        reservation.save()

        book.availability -= 1
        book.save()
        return reservation

    @staticmethod
    def hand_book(reservation_id):
        
        reservation = Reservation.objects.get(id=reservation_id)
        if reservation.handed:
            raise ValueError("Book has already been handed.")
        
        reservation.handed = True
        reservation.save()
        
    @staticmethod
    def overdue(reservation_id):
        reservation = Reservation.objects.get(id=reservation_id)

        if reservation.handed:
            raise ValueError("Cannot mark handed book as overdue.")
        
        reservation.book.availability += 1
        reservation.overdued = True
        reservation.book.save()