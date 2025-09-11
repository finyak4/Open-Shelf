from django.urls import path
from . import views

urlpatterns = [
    path('', views.library, name="library"),
    path('book/<int:id>/', views.book_view, name="book_page"),
    path('reservation/<int:id>/reserve/', views.reserve, name="reserve"),
    path('reservation/<int:id>/', views.reservation_page, name="reservation_page"),
    ]