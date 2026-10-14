from django import forms
from .models import Upload, ProfileData, WorkoutDrill, Session, Macrocycle, ProfileMacrocycle, TrainingTheme, TrainingWeek, TrainingBlock, TestName, TrainingBlock, MenuCategory, MenuSubCategory, ClientCategory, Status, Attendance

class UploadForm(forms.ModelForm):
    class Meta:
        model = Upload
        fields = ['title', 'file']

class NewAthleteForm(forms.ModelForm):
    class Meta:
        model = ProfileData
        fields = ['first_name', 'middle_name', 'last_name' ,'DOB', 'weight', 'height', 'client_category', 'status', 'image']
        

class NewWorkoutDrillForm(forms.ModelForm):
    class Meta:
        model = WorkoutDrill
        fields = ['name', 'sets', 'repetitions', 'distance', 'duration', 'prescription', 'description']

class NewSessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['name','session_type', 'menu_type', 'date', 'location', 'drills']

class NewMacrocycleForm(forms.ModelForm):
    class Meta:
        model = Macrocycle
        fields = ['name', 'estimated_weeks', 'description']

class NewProfileMacrocycleForm(forms.ModelForm):
    class Meta:
        model = ProfileMacrocycle
        fields = ['macrocycle', 'profile', 'season_phase', 'program_phase', 'start_date']

class NewTestForm(forms.ModelForm):
    class Meta:
        model = TestName
        fields = ['name', 'quality', 'protocol', 'unit', 'direction', 'attempts', 'equipment', 'classification']

class NewTrainingThemeForm(forms.ModelForm):
    class Meta:
        model = TrainingTheme
        fields = ['macrocycle', 'name', 'start_week', 'end_week', 'description']



class NewTrainingBlockForm(forms.ModelForm):
    class Meta:
        model =TrainingBlock
        fields = ['theme', 'start_week', 'end_week', 'name', 'description']

class NewMenuCategoryForm(forms.ModelForm):
    class Meta:
        model = MenuCategory
        fields = ['code', 'name', 'description', 'notes']

class NewMenuSubCategory(forms.ModelForm):
    class Meta:
        model = MenuSubCategory
        fields = ['category', 'code', 'title', 'subtitle', 'best_for', 'notes']

# forms.py
class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['block', 'week', 'session', 'notes']

    def __init__(self, *args, **kwargs):
        profile_macrocycle = kwargs.pop('profile_macrocycle', None)
        super().__init__(*args, **kwargs)

        if profile_macrocycle:
            # Filter weeks
            self.fields['week'].queryset = TrainingWeek.objects.filter(
                macrocycle=profile_macrocycle
            )

            # Filter blocks
            self.fields['block'].queryset = TrainingBlock.objects.filter(
                theme__macrocycle=profile_macrocycle
            )

            
