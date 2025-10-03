from . import models
from django import forms
from library.models import Genre, Author, Book
from difflib import get_close_matches

class AddBook(forms.ModelForm):
    genre = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    author = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = models.Book
        fields = ['title', 'description', 'author' , 'availability', 'publication_year', 'genre', 'cover_image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
 
            field.widget.attrs['placeholder'] = " "

    def clean_author(self):
        author_name = self.cleaned_data.get('author', '').strip()
        if not author_name:
            return None

        existing_authors = list(Author.objects.values_list('name', flat=True))
        close_matches = get_close_matches(author_name, existing_authors, n=1, cutoff=0.8)
        if close_matches:
            author_obj = Author.objects.get(name=close_matches[0])
        else:
            author_obj = Author.objects.create(name=author_name)

        return author_obj

    def clean_genre(self):
        name = self.cleaned_data.get('genre', '').strip()
        if not name:
            return None

        existing_genres = list(Genre.objects.values_list('name', flat=True))
        match = get_close_matches(name, existing_genres, n=1, cutoff=0.8)
        if match:
            return Genre.objects.get(name=match[0])
        else:
            return Genre.objects.create(name=name)   