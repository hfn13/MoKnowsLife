from django.shortcuts import render, redirect

from .models import ProfileData,Session,Attendance,TrackTest,TrackTestData,LiftTest,LiftTestData,WorkoutDrill, Upload, MenuCategory, MenuSubCategory, PhaseChoice, BlockChoice,MenuOption

from .forms import UploadForm

# Create your views here.
def ngoma_home(request):
    'Ngoma Fitness home.'
    return render(request, 'ngoma_index.html')

def workout_library(request):
    phases = PhaseChoice.objects.all()
    blocks = BlockChoice.objects.all()

    block_by_phase = {}
    for phase in phases:
        block_by_phase[phase] = blocks.filter(phase=phase)

    context = {
        'phases' : phases,
        'blocks' : blocks,
        'block_by_phase' : block_by_phase
    }
    return render(request, 'workout_library.html', context)

def phase_view(request, phase_id):
    phase = PhaseChoice.objects.get(id=phase_id)
    blocks = BlockChoice.objects.filter(phase=phase)

    context = {
        'phase' : phase,
        'blocks' : blocks
    }

    return render(request, 'phase_view.html', context)


def block_view(request, block_id):
    drill_block = BlockChoice.objects.get(id=block_id)
    drills = WorkoutDrill.objects.filter(block = drill_block)

    context = {
        'drill_block' : drill_block,
        'drills' : drills
    }

    return render(request, 'block_view.html', context)

def menu_library(request):
    'Ngoma Fiteness workout plan.'
    menus = MenuCategory.objects.all()
    sub_cats = MenuSubCategory.objects.all()

    sub_cat_by_menu = {}
    for menu in menus:
        sub_cat_by_menu[menu] = sub_cats.filter(category=menu)

    context = {
        'menus' : menus,
        'sub_cats' : sub_cats,
        'sub_cat_by_menu' : sub_cat_by_menu
    }
    return render(request, 'menu_library.html', context)

def menucategory(request, cat_id):
    menu = MenuCategory.objects.get(id=cat_id)
    submenus = menu.menusubcategory_set.all()
    notes = menu.notes

    context = {
        'menu' : menu,
        'submenus' : submenus,
        'notes' : notes
    }
    
    return render(request, 'menu_category.html', context)

def menusubcategory(request, subcat_id):
    submenu = MenuSubCategory.objects.get(id=subcat_id)
    menu = submenu.category

    blocks = MenuOption.objects.filter(category=submenu)
    context = {
        'submenu' : submenu,
        'menu' : menu,
        'blocks' : blocks
    }
    return render(request, 'menu_subcategory.html', context)


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
    submenu_df = pd.read_csv(r"C:\Users\cex\Desktop\moknowslife\DETAILED_MENU_OPTIONS.csv")
    workouts_df = pd.read_csv(r"C:\Users\cex\Desktop\moknowslife\workouts.csv")
    phases_df = pd.read_csv(r"C:\Users\cex\Desktop\moknowslife\phases.csv")
    blocks_df = pd.read_csv(r"C:\Users\cex\Desktop\moknowslife\blocks.csv")

    for _, phase_row in phases_df.iterrows():
        phase, _ = PhaseChoice.objects.get_or_create(
            phase=phase_row['phase'],
            order=phase_row['order']
        )
    

        for _, block_row in blocks_df.iterrows():
            BlockChoice.objects.get_or_create(
                phase = phase,
                block=block_row['blocks']
                
            )
    
    for _, workout_row in workouts_df.iterrows():
        if workout_row['Phase'] == 'Build':
            order = 2
        elif workout_row['Phase'] == 'Base':
            order = 1
        elif workout_row['Phase'] == 'Peak':
            order = 3
        phase, _ = PhaseChoice.objects.get_or_create(
            phase=workout_row['Phase'],
            order = order
        )
        block, _ = BlockChoice.objects.get_or_create(
            phase = phase,
            block=workout_row['Block']
        )
        WorkoutDrill.objects.get_or_create(
            
            name = workout_row['Name'],
            sets = workout_row['Sets'],
            repetitions = workout_row['Reps'],
            distance = workout_row['Distance'],
            duration = workout_row['Duration'],
            block = block,
            prescription = workout_row['Original Prescription']
        )

    for _, menu_row in menu_df.iterrows():
        menu, _ = MenuCategory.objects.get_or_create(
            code=menu_row['code'],
            name=menu_row['name'],
            notes = menu_row['notes']
        )

        # Filter submenu rows that belong to this menu
        related_submenus = submenu_df[submenu_df['category'] == menu_row['code']]

        for _, sub_row in related_submenus.iterrows():
            MenuSubCategory.objects.get_or_create(
                category=menu,
                code=sub_row['code'],
                title=sub_row['title'],
                subtitle=sub_row['subtitle']
            )

    
    return redirect('ngoma:workout_library')

def update_submenu(request, submenu_id):
    import pandas as pd
    menublocks_df = pd.read_csv(r"C:\Users\cex\Desktop\moknowslife\MENUBLOCKS_df.csv")
    submenu = MenuSubCategory.objects.get(id=submenu_id)
    code = submenu.code
    related_df = menublocks_df[menublocks_df['SubCategory'] == code]
    
    for _, rows in related_df.iterrows():
        num = rows['Category_number']
        block_full = f"{rows['Block']} {int(num)}" if pd.notna(num) else rows['Block']
        MenuOption.objects.get_or_create(
            category = submenu,
            block = block_full
        )

    return redirect('ngoma:menu_subcategory', submenu_id)