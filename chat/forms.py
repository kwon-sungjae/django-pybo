# chat/forms.py
from django import forms

class MessageForm(forms.Form):
    content = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type a message'}))