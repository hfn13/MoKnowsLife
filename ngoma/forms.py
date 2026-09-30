from django import forms
from .models import Upload, ProfileData, WorkoutDrill, Session

class UploadForm(forms.ModelForm):
    class Meta:
        model = Upload
        fields = ['title', 'file']

class NewAthleteForm(forms.ModelForm):
    class Meta:
        model = ProfileData
        fields = ['first_name', 'middle_name', 'last_name' ,'DOB', 'weight', 'height']

class NewWorkoutDrillForm(forms.ModelForm):
    class Meta:
        model = WorkoutDrill
        fields = ['name', 'sets', 'repetitions', 'distance', 'duration', 'prescription', 'description']

class NewSessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['session_type', 'date', 'time', 'location', 'drills']