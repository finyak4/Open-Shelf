from django.db import models
from home.models import User
import datetime
from django.utils import timezone
from django.utils.timezone import now


# Create your models here.
# class Borrowing(models.Model):
#     class Meta:
#         verbose_name = "Borrowing"
#         verbose_name_plural = "Borrowings"
#         db_table = "borrowings"

#     from library.models import Book
#     books = models.ManyToManyField(Book, related_name="borrowing")
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     borrow_date = models.DateTimeField(auto_now_add=True)
#     return_date = models.DateTimeField(null=True, blank=True)
#     due_to = models.DateTimeField()

#     @classmethod
#     def create(cls, user, books):
#         borrow = cls.objects.create(
#             user=user,
#             due_to= timezone.now() + datetime.timedelta(days=21) 
#         )
#         borrow.books.set(books)

#         return borrow
    
#     @staticmethod
#     def return_book(borrowing_id):
#         borrowing = Borrowing.objects.get(id = borrowing_id)
#         borrowing.return_date = now()
#         borrowing.save()

#         for book in borrowing.books.all():
#             book.availability += 1
#             book.save()


        