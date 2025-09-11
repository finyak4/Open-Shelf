from django.db import models
from home.models import User
from .validators import validate_four_digits

class Genre(models.Model):
    name = models.CharField(max_length=64, unique=True)

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"
        db_table = "genres"

    def __str__(self):
        return self.name

class Book(models.Model):    
    title = models.CharField(max_length=128)
    author = models.CharField( max_length=128)
    description = models.CharField(max_length=512)
    availability = models.PositiveIntegerField(default=0)
    publication_year = models.PositiveIntegerField(validators=[validate_four_digits])
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, related_name="books")
    cover_image = models.URLField ()

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"
        db_table = "books"    

class Reservation(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    handed = models.BooleanField(default=False)
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
        reservation.book.save()

        reservation.delete()
