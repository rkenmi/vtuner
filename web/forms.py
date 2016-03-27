from django import forms
from models import MP3

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = MP3
        fields = ['mp3file']
