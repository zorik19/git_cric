from django.forms import ModelForm
from django import forms
from .models import Images


class ImageForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = '__all__'
        labels = {'photo': ''}
        textwrap = {'No file chosen': ''}
