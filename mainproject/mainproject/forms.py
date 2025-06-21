from django import forms
from myapp.models import *

class EventForm(forms.ModelForm):
    class Meta:
        model = Events
        fields = ['image','year','description']

