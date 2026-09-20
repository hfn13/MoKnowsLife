from django.shortcuts import render, redirect
from django.utils import timezone
from .models import ProfileData,Session,Attendance,TrackTest,TrackTestData,LiftTest,LiftTestData,WorkoutDrill, Upload, MenuCategory, MenuSubCategory, PhaseChoice, BlockChoice,MenuOption, TrendAnalyses, TrendTest, CISTI_score, TrendTestData

from .forms import UploadForm,NewAthleteForm

now = timezone.now()
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

    submenu_by_cat = {}
    for submenu in submenus:
        submenu_by_cat[submenu] = MenuOption.objects.filter(category=submenu)
        
    import ast

    raw_notes = menu.notes or "[]"
    notes = ast.literal_eval(raw_notes)
    notes = [note.split(':') for note in notes]

    

    context = {
        'menu' : menu,
        'submenus' : submenus,
        'notes' : notes,
        'submenu_by_cat' : submenu_by_cat
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


# def athletes(request):
#     'List of signed up athletes'
#     return render(request, 'athletes.html')

# def athlete(request, athlete_id):
#     'Athlete Dashboard to track progress'
#     athlete = ProfileData.objects.get(id=athlete_id)

#     context = {
#         'athlete' : athlete
#     }
#     return render(request, 'athlete.html', context)

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
    track_df = pd.read_csv(r"C:\Users\cex\Desktop\moknowslife\Track_tests.csv")
    lift_df = pd.read_csv(r"C:\Users\cex\Desktop\moknowslife\Lift_tests.csv")

    trend_test = ['100','150','150 Float Fly','200 Float Fly','200 Breakdowns','200','300', '2x100m', '3x300m', '2x150m', '200m Breakdown', '200m Split', '200m @ 85%']
    trend_test_df = pd.DataFrame(trend_test, columns=['Test'])
    
    trend_analyses = ['Performance vs Distance', 'Drop % vs Distance', 'Consistency vs Distance', 'Effort vs Time']
    trend_analyses_df = pd.DataFrame(trend_analyses, columns=['Analyses'])

    
    for _,trackt_row in track_df.iterrows():
        TrackTest.objects.get_or_create(
            test = trackt_row['test']
        )


    for _,liftt_row in lift_df.iterrows():
        LiftTest.objects.get_or_create(
            test = liftt_row['test']
        )
    
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



    trend_tests_df = pd.read_csv(r"C:\Users\cex\Desktop\moknowslife\trend_tests.csv")
    for _,row in trend_tests_df.iterrows():
        LiftTest.objects.get_or_create(
                test = row['Test']
            ) 

    for _,row in trend_analyses_df.iterrows():
        TrendAnalyses.objects.get_or_create(
            analyses = row['Analyses']
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


def athletes(request):
    athletes = ProfileData.objects.all()

    context = {
        'athletes' : athletes
    }

    return render(request, 'athletes.html', context)

def athlete(request, athlete_id):
    #Athlete Dashboard
    from datetime import date
    athlete = ProfileData.objects.get(id=athlete_id)
    today = date.today()

    age = today.year - athlete.DOB.year - (
        (today.month, today.day) < (athlete.DOB.month, athlete.DOB.day)
    )
    
    
    track_data = TrackTestData.objects.filter(profile=athlete)
    track_tests = TrackTest.objects.all()
    lift_data = LiftTestData.objects.filter(profile=athlete)
    lift_tests = LiftTest.objects.all()

    track_summary = {}

    for test in track_tests:
        test_results = track_data.filter(test=test).order_by('date')

        if test_results.exists():
            values = [d.value for d in test_results]

            track_summary[test] = {
                'fastest': min(values),
                'slowest': max(values),
                'latest': test_results.last().value
            }
        else:
            track_summary[test] = {
                'fastest': 0,
                'slowest': 0,
                'latest': 0
            }
    

    lift_summary = {}

    for test in lift_tests:
        test_results = lift_data.filter(test=test).order_by('date')

        if test_results.exists():
            values = [d.value for d in test_results]

            lift_summary[test] = {
                'fastest': min(values),
                'slowest': max(values),
                'latest': test_results.last().value
            }
        else:
            lift_summary[test] = {
                'fastest': 0,
                'slowest': 0,
                'latest': 0
            }

    #Trends
    trend_analyses = TrendAnalyses.objects.all()
    trend_tests = TrendTestData.objects.filter(profile=athlete)
    
    trend_tables = {}
    
    for analyses in trend_analyses:
        analyses_tests = trend_tests.filter(analyses=analyses).order_by('date')
    
        # Extract unique test names
        test_names = list(
            analyses_tests.values_list('test__test', flat=True).distinct()
        )
    
        # Extract unique dates
        dates = list(
            analyses_tests.values_list('date', flat=True).distinct()
        )
    
        # Build table rows
        rows = []
        for date in dates:
            row = {'date': date, 'values': []}
    
            for test_name in test_names:
                value_obj = analyses_tests.filter(
                    date=date,
                    test__test=test_name
                ).first()
    
                row['values'].append(value_obj.value if value_obj else '')
    
            rows.append(row)
    
        trend_tables[analyses.analyses] = {
            'tests': test_names,
            'rows': rows
        }

    context = {
        'athlete' : athlete,
        'age' : age,
        'track_tests':track_tests,
        'track_data' : track_data,
        'track_summary':track_summary,
        'lift_tests':lift_tests,
        'lift_data' : lift_data,
        'lift_summary':lift_summary,
        'trend_analyses':trend_analyses,
        'trend_tests':trend_tests,
        'trend_tables':trend_tables
    }

    return render(request, 'athlete.html', context)


def new_athlete(request):
    if request.method == 'POST':
        form = NewAthleteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('ngoma:athletes')
    else:
        form = NewAthleteForm()

    return render(request, 'newathlete.html', {'form': form})


athletes_data = {
    'Henry Nyinguro' : {'lift' : r"C:\Users\cex\Desktop\moknowslife\Track_DummyData.csv",
                        'track' : r"C:\Users\cex\Desktop\moknowslife\Lift_DummyData.csv",
                        #Trend analyses
                        'Consistency vs Distance':r"C:\Users\cex\Desktop\moknowslife\Consistency vs Distance.csv",
                        'Effort vs Time':r"C:\Users\cex\Desktop\moknowslife\Effort vs Time.csv",
                        'Performance vs Distance':r"C:\Users\cex\Desktop\moknowslife\Performance vs Distance.csv",
                        'Drop % vs Distance':r"C:\Users\cex\Desktop\moknowslife\Drop % vs Distance.csv"
                       }
}
def update_athlete_profile(request, athlete_id):
    athlete = ProfileData.objects.get(id=athlete_id)
    athlete_string = f'{athlete.first_name} {athlete.last_name}'

    
    # Lift data
    lift_df = pd.read_csv(athletes_data[athlete_string]['lift'])

    lift_tests = lift_df.columns.difference(['Date','Unnamed: 0'])
    for _, row in lift_df.iterrows():
        for test in lift_tests:
            test_obj, _ = LiftTest.objects.get_or_create(
                test = test
            )
            value = row[test]
            if pd.isna(value): 
                continue
                
            LiftTestData.objects.get_or_create(
                profile = athlete,
                test = test_obj,
                date= row['Date'],
                value = value
            )
    
    # Track data
    track_df = pd.read_csv(athletes_data[athlete_string]['track'])
    track_tests = track_df.columns.difference(['Date','Unnamed: 0'])
    for _, row in track_df.iterrows():
        for test in track_tests:
            test_obj, _ = TrackTest.objects.get_or_create(
                test = test
            )
            value = row[test]
            if pd.isna(value):
                continue
                
            TrackTestData.objects.get_or_create(
                profile = athlete,
                test = test_obj,
                date= row['Date'],
                value = value
            )



    ### Trend Analyses
    # Consistency vs Distance
    con_v_dist = pd.read_csv(athletes_data[athlete_string]['Consistency vs Distance'])
    cvd_tests = con_v_dist.columns.difference(['Unnamed: 0'])
    cvd_analyses = TrendAnalyses.objects.get(analyses='Consistency vs Distance')
    for _, row in con_v_dist.iterrows():
        for test in cvd_tests:
            test_obj, _ = TrendTest.objects.get_or_create(
                test = test
            )
            value = row[test]
            if pd.isna(value):
                continue
                
            TrendTestData.objects.get_or_create(
                profile = athlete,
                analyses = cvd_analyses,
                test = test_obj,
                value = value
            )
    
    # Effort vs Time
    eff_v_time = pd.read_csv(athletes_data[athlete_string]['Effort vs Time'])
    evt_tests = eff_v_time.columns.difference(['Unnamed: 0'])
    evt_analyses = TrendAnalyses.objects.get(analyses='Effort vs Time')
    for _, row in eff_v_time.iterrows():
        for test in evt_tests:
            test_obj, _ = TrendTest.objects.get_or_create(
                test = test
            )
            value = row[test]
            if pd.isna(value):
                continue
                
            TrendTestData.objects.get_or_create(
                profile = athlete,
                analyses = evt_analyses,
                test = test_obj,
                value = value
            )
            
    # Performance vs Distance
    perf_v_dist = pd.read_csv(athletes_data[athlete_string]['Performance vs Distance'])
    pvd_tests = perf_v_dist.columns.difference(['Unnamed: 0'])
    pvd_analyses = TrendAnalyses.objects.get(analyses='Performance vs Distance')
    for _, row in perf_v_dist.iterrows():
        for test in pvd_tests:
            test_obj, _ = TrendTest.objects.get_or_create(
                test = test
            )
            value = row[test]
            if pd.isna(value):
                continue
                
            TrendTestData.objects.get_or_create(
                profile = athlete,
                analyses = pvd_analyses,
                test = test_obj,
                value = value
            )
    
    # Drop % vs Distance
    drop_v_dist = pd.read_csv(athletes_data[athlete_string]['Drop % vs Distance'])
    dvd_tests = drop_v_dist.columns.difference(['Unnamed: 0'])
    dvd_analyses = TrendAnalyses.objects.get(analyses='Drop % vs Distance')
    for _, row in drop_v_dist.iterrows():
        for test in dvd_tests:
            test_obj, _ = TrendTest.objects.get_or_create(
                test = test
            )
            value = row[test]
            if pd.isna(value):
                continue
                
            TrendTestData.objects.get_or_create(
                profile = athlete,
                analyses = dvd_analyses,
                test = test_obj,
                value = value
            )
    
    
    return redirect('ngoma:athlete', athlete_id)