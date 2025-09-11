from . import models
from django import forms
from .models import Genre

class AddBook(forms.ModelForm):
    genre = forms.ModelChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    class Meta:
        model = models.Book
        fields = ['title', 'description', 'author' , 'availability', 'publication_year', 'genre', 'cover_image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
 
            field.widget.attrs['placeholder'] = " "