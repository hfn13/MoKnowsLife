from django import forms
from .models import Upload, ProfileData

class UploadForm(forms.ModelForm):
    class Meta:
        model = Upload
        fields = ['title', 'file']

class NewAthleteForm(forms.ModelForm):
    class Meta:
        model = ProfileData
        fields = ['first_name', 'middle_name', 'last_name' ,'DOB', 'weight', 'height']