from . import models
from django import forms
from library.models import Genre, Author, Book
from difflib import get_close_matches

class AddBook(forms.ModelForm):
    genre = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    author = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = models.Book
        fields = ['title', 'description' , 'availability', 'publication_year', 'cover_image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
 
            field.widget.attrs['placeholder'] = " "
