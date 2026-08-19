from django.shortcuts import render, redirect

from .models import ProfileData,Session,Attendance,TrackTest,TrackTestData,LiftTest,LiftTestData,WorkoutDrill, Upload, MenuCategory, MenuSubCategory

from .forms import UploadForm

# Create your views here.
def ngoma_home(request):
    'Ngoma Fitness home.'
    return render(request, 'ngoma_index.html')

def workout_library(request):
    'Ngoma Fiteness workout plan.'
    menus = MenuCategory.objects.all()
    sub_cats = MenuSubCategory.objects.all()

    sub_cat_by_menu = {}
    for menu in menus:
        sub_cat_by_menu[menu.id] = sub_cats.filter(category=menu)

    context = {
        'menus' : menus,
        'sub_cats' : sub_cats,
        'sub_cat_by_menu' : sub_cat_by_menu
    }
    return render(request, 'workout_library.html', context)

def athletes(request):
    'List of signed up athletes'
    return render(request, 'athletes.html')

def athlete(request, athlete_id):
    'Athlete Dashboard to track progress'
    athlete = ProfileData.objects.get(id=athlete_id)

    context = {
        'athlete' : athlete
    }
    return render(request, 'athlete.html', context)

def forms_display(request):
    forms = Upload.objects.all()

    context = {
        'forms' : forms
    }
    return render(request, 'forms_display.html', context)

def upload_success(request):
    files = Upload.objects.all()
    return render(request, 'upload_success.html', {'files': files})

def upload_file(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('ngoma:forms_display')
    else:
        form = UploadForm()

    return render(request, 'upload.html', {'form': form})


import pandas as pd

def update_menuoptions(request):
    menu_df = pd.read_csv(r"C:\Users\cex\Desktop\moknowslife\MENU_OPTIONS.csv")
    for _, row in menu_df.iterrows():
        MenuCategory.objects.get_or_create(
            code = row['code'],
            name = row['name']
        )
    return redirect('ngoma:workout_library')