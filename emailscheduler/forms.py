from django import forms
from .models import Email

class ContactForm(forms.ModelForm):
    email = forms.EmailField()
    subject = forms.CharField()
    message = forms.CharField()
    time = forms.IntegerField()

    class Meta:
        model = Email
        fields = ('email',)