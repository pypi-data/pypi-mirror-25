from django import forms
from .models import Image


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('caption', 'file',)
