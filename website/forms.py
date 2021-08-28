from django import forms

class NameForm(forms.Form):
    search_term = forms.CharField(label='Search_Term', max_length=100)
