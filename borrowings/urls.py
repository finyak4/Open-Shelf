from django.urls import path
from . import views

urlpatterns = [
    path('', views.borrowings, name="borrowings"),
    path('borrow/', views.borrow, name="borrow"),
    path('borrow_man/', views.borrow_man, name="borrow_man"),
    path('autocomplete/', views.autocomplete, name='autocomplete'),
    path('autocomplete_books/', views.autocomplete_books, name="autocomplete_books"),
    ]