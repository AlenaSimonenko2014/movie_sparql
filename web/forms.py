from django import forms


class SearchForm(forms.Form):
    movie_name = forms.CharField(max_length=128)
