from django.shortcuts import render, redirect
from django.utils import timezone
from .models import ProfileData,Session,Attendance,TrackTest,TrackTestData,LiftTest,LiftTestData,WorkoutDrill, Upload, MenuCategory, MenuSubCategory, PhaseChoice, BlockChoice,MenuOption, TrendAnalyses, TrendTest, CISTIScore, TrendTestData, Macrocycle, ProfileMacrocycle, ClientCategory, Status, TrainingWeek, WorkoutCategory, Attendance, TrainingTheme, TrainingBlock
from django.http import JsonResponse
import calendar
from calendar import HTMLCalendar
from .forms import UploadForm,NewAthleteForm
from ngoma.utils.calendar import WorkoutCalendar

now = timezone.now()
# Create your views here.

## Home Page
from datetime import date
from ngoma.utils.calendar import WorkoutCalendar

def ngoma_index(request):
    today = date.today()

    # Read month/year from query parameters
    year = int(request.GET.get("year", today.year))
    month = int(request.GET.get("month", today.month))

    # Build event dictionary
    events = {}
    for session in Session.objects.all():
        events.setdefault(session.date.isoformat(), []).append(session)

    cal = WorkoutCalendar(events).formatmonth(year, month)

    # Calculate previous/next month
    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1

    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1

    return render(request, "ngoma_index.html", {
        "cal": cal,
        "year": year,
        "month": month,
        "prev_year": prev_year,
        "prev_month": prev_month,
        "next_year": next_year,
        "next_month": next_month,
    })


def events_for_date(request, date):
    events = Session.objects.filter(date=date)
    data = {
        'events': [{'name': e.name} for e in events]
    }
    return JsonResponse(data)


## 

## Workouts Page

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

def drill(request, drill_id):
    drill = WorkoutDrill.objects.get(id = drill_id)
    instances = {
        'sets' : drill.sets,
        'repetitions' : drill.repetitions,
        'block' : drill.block,
        'name' : drill.name,
        'distance' : drill.distance,
        'duration' : drill.duration,
        'prescription' : drill.prescription,
        'description' : drill.description
    }

    for name, instance in instances.items():
        if instance is None:
            instances[name] = 'Not Applicable (N/A)'

    context = {
        'drill' : drill,
        'instances' : instances
    }   

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


def tests_display(request):
    tests = TestName.objects.all()

    context = {
        'tests' : tests
    }
    return render(request, 'test_display.html', context)

def test_display(request, test_id):
    test = TestName.objects.get(id=test_id)

    context = {
        'test' : test
    }
    return render(request, 'test_display.html', context)

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



### DASHBOARDS
from django.utils.timezone import now

def ngoma_dashboard(request):
    macrocycles = ProfileMacrocycle.objects.all()
    sessions = Session.objects.all()

    today = now().date()

    current_macrocycles = []
    ended_macrocycles = []

    
    for macrocycle in macrocycles:
        from datetime import timedelta
        
        weeks = macrocycle.macrocycle.estimated_weeks
        days = int(weeks) * 7
        
        estimated_end_date = macrocycle.start_date + timedelta(days=days)
 
        if estimated_end_date > today:
            current_macrocycles.append(macrocycle)
        else:
            ended_macrocycles.append(macrocycle)

    upcoming_sessions = []
    past_sessions = []

    for session in sessions:
        if session.date.date() > today:
            upcoming_sessions.append(session)
        else:
            past_sessions.append(session)

    context = {
        'macrocycles': macrocycles,
        'current_macrocycles': current_macrocycles,
        'ended_macrocycles': ended_macrocycles,
        'upcoming_sessions': upcoming_sessions,
        'past_sessions': past_sessions,
        'date' : today
    }

    return render(request, 'ngoma_dashboard.html', context)

def macrocycles(request):
    macrocycles = Macrocycle.objects.all()

    context = {
        'macrocycles' : macrocycles
    }

    return render(request, 'macrocycles.html', context)
    
def macrocycle(request, macrocycle_id):
    macrocycle = Macrocycle.objects.get(id=macrocycle_id)
    profiles = ProfileMacrocycle.objects.filter(macrocycle = macrocycle)

    def generate_training_weeks(profile_macrocycle):
        mc = profile_macrocycle.macrocycle  # Macrocycle object
    
        start = profile_macrocycle.start_date
        weeks = mc.estimated_weeks
    
        for week in range(1, int(weeks)):
            TrainingWeek.objects.update_or_create(
                macrocycle = profile_macrocycle,
                week_number = week
            )
            
    
    context = {
        'macrocycle' : macrocycle,
        'profiles' : profiles
    }
    return render(request, 'macrocycle.html', context)

def sessions(request):
    sessions = Session.objects.all()

    context = {
        'sessions' : sessions
    }

    return render(request, 'sessions.html', context)
    
def session(request, session_id):
    session = Session.objects.get(id=session_id)

    context = {
        'session' : session
    }
    return render(request, 'session.html', context)

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
    category = athlete.client_category
    availability = athlete.status
    image = athlete.image
    today = date.today()

    age = today.year - athlete.DOB.year - (
        (today.month, today.day) < (athlete.DOB.month, athlete.DOB.day)
    )
    macrocycles = ProfileMacrocycle.objects.filter(profile=athlete).order_by('-start_date')

    

    selected_id = request.GET.get("macrocycle_id")
    
    # CASE 1: Athlete has no macrocycles at all
    if not macrocycles.exists():
        macrocycle = None
        macrocycle_obj = None
        season_phase = None
        program_phase = None
        training_weeks = None
        week = None
        theme = None
        block = None
        
    else:
        # CASE 2: Athlete selected a macrocycle
        if selected_id:
            try:
                macrocycle = ProfileMacrocycle.objects.get(id=selected_id, profile=athlete)
            except ProfileMacrocycle.DoesNotExist:
                macrocycle = macrocycles.first()
        else:
            # CASE 3: Default to latest macrocycle
            macrocycle = macrocycles.first()

        
        macrocycle_obj = macrocycle.macrocycle

        season_phase = macrocycle.season_phase
        program_phase = macrocycle.program_phase
        training_weeks = macrocycle.macrocycle.estimated_weeks

        def get_current_training_week(profile_macrocycle):
            weeks = TrainingWeek.objects.filter(macrocycle=profile_macrocycle).order_by("week_number")
        
            # If no weeks exist, create week 1
            if not weeks.exists():
                week1, _ = TrainingWeek.objects.get_or_create(
                    macrocycle=profile_macrocycle,
                    week_number=1,
                    defaults={"completed": False}
                )
                return week1
        
            # Find first incomplete week
            for week in weeks:
                if not week.completed:
                    return week
        
            # If all weeks are complete → return last week
            return weeks.last()

        
        week = get_current_training_week(macrocycle)
        
        theme=TrainingTheme.objects.filter(
            start_week__week_number__lte=week.week_number,
            end_week__week_number__gte=week.week_number).first()
        
        block = TrainingBlock.objects.filter(
            start_week__week_number__lte=week.week_number,
            end_week__week_number__gte=week.week_number
        ).first()


        
   
    # track_data = TrackTestData.objects.filter(profile=athlete)
    # track_tests = TrackTest.objects.all()
    # lift_data = LiftTestData.objects.filter(profile=athlete)
    # lift_tests = LiftTest.objects.all()

    # track_summary = {}

    # for test in track_tests:
    #     test_results = track_data.filter(test=test).order_by('date')

    #     if test_results.exists():
    #         values = [d.value for d in test_results]

    #         track_summary[test] = {
    #             'fastest': min(values),
    #             'slowest': max(values),
    #             'latest': test_results.last().value
    #         }
    #     else:
    #         track_summary[test] = {
    #             'fastest': 0,
    #             'slowest': 0,
    #             'latest': 0
    #         }
    

    # lift_summary = {}

    # for test in lift_tests:
    #     test_results = lift_data.filter(test=test).order_by('date')

    #     if test_results.exists():
    #         values = [d.value for d in test_results]

    #         lift_summary[test] = {
    #             'fastest': min(values),
    #             'slowest': max(values),
    #             'latest': test_results.last().value
    #         }
    #     else:
    #         lift_summary[test] = {
    #             'fastest': 0,
    #             'slowest': 0,
    #             'latest': 0
    #         }

    # #Trends
    # trend_analyses = TrendAnalyses.objects.all()
    # trend_tests = TrendTestData.objects.filter(profile=athlete)
    
    # trend_tables = {}
    
    # for analyses in trend_analyses:
    #     analyses_tests = trend_tests.filter(analyses=analyses).order_by('date')
    
    #     # Extract unique test names
    #     test_names = list(
    #         analyses_tests.values_list('test__test', flat=True).distinct()
    #     )
    
    #     # Extract unique dates
    #     dates = list(
    #         analyses_tests.values_list('date', flat=True).distinct()
    #     )
    
    #     # Build table rows
    #     rows = []
    #     for date in dates:
    #         row = {'date': date, 'values': []}
    
    #         for test_name in test_names:
    #             value_obj = analyses_tests.filter(
    #                 date=date,
    #                 test__test=test_name
    #             ).first()
    
    #             row['values'].append(value_obj.value if value_obj else '')
    
    #         rows.append(row)
    
    #     trend_tables[analyses.analyses] = {
    #         'tests': test_names,
    #         'rows': rows
    #     }

    context = {
        
        'athlete' : athlete,
        'age' : age,
        'image' : image,
        'category' : category,
        'availability' : availability,
        'macrocycles' : macrocycles,
        'macrocycle' : macrocycle,
        'season_phase' : season_phase,
        'program_phase' : program_phase,
        'training_weeks' : training_weeks,
        'week' : week,
        'theme' : theme,
        'block' : block
        # 'track_tests':track_tests,
        # 'track_data' : track_data,
        # 'track_summary':track_summary,
        # 'lift_tests':lift_tests,
        # 'lift_data' : lift_data,
        # 'lift_summary':lift_summary,
        # 'trend_analyses':trend_analyses,
        # 'trend_tests':trend_tests,
        # 'trend_tables':trend_tables,
        
    }

    return render(request, 'athlete.html', context)

    
def tests_display(request):
    tests = TestName.objects.all()

    context = {
        'tests' :tests
    }

    return render(request, 'tests_display.html', context)

def test_display(request, test_id):
    test = TestName.objects.get(id=test_id)

    context = {
        'test' : test
    }
    return render(request, 'test_display.html', context)


def training_themes(request):
    themes = TrainingTheme.objects.all()
    theme_duration_dict = {}
    for theme in themes:
        theme_duration_dict[theme] = int(theme.end_week) - int(theme.start_week)
    
    context = {
        'themes' : themes
    }
    return render(request, 'training_themes.html', context)


def profile_trainingthemes(request, profile_id):
    macrocycle = ProfileMacrocycle.objects.get(id=profile_id)
    themes = TrainingTheme.objects.filter(macrocycle = macrocycle)
    profile = macrocycle.profile
    blocks = TrainingBlock.objects.all()

    theme_dict = {}
    for theme in themes:
        theme_dict[theme] = int(theme.end_week.week_number) - int(theme.start_week.week_number)
        theme_dict[theme] = blocks.filter(theme=theme)
        
    context = {
        'profile' : profile,
        'themes' : themes,
        'macrocycle' : macrocycle,
        'theme_dict' : theme_dict
    }
    return render(request, 'profile_trainingthemes.html', context)
    
def training_theme(request, theme_id):
    theme = TrainingTheme.objects.get(id=theme_id)
    profiles = theme.profile_set.all()
    
    context = {
        'theme' : theme,
        'profiles' : profiles
    }
    return render(request, 'training_theme.html', context)
    
def training_blocks(request):
    blocks = TrainingBlock.objects.all()
    
    block_info_dict = {}
    for block in blocks:
        block_info_dict[block] = int(block.end_week) - int(block.start_week)
        
        
    context = {
        'blocks' : blocks,
        'block_info_dict' : block_info_dict
    }
    
    return render(request, 'training_blocks.html', context)

def profile_trainingblocks(request, theme_id):
    theme = TrainingTheme.objects.get(id=theme_id)
    blocks = TrainingBlock.objects.filter(theme=theme)
    macrocycle = theme.macrocycle
    

    context = {
        'profile' : profile,
        'blocks' : blocks 
    }
    return render(request, 'profile_trainingblocks.html', context)


def training_block(request, block_id):
    block = TrainingBlock.objects.all()
    themes = block.theme_set.all()
    sessions = Attendance.objects.filter(block = block)
    
    context = {
        'block' : block,
        'themes' : themes
    }
    return render(request, 'training_block.html', context)


def complete_week(request, week_id):
    week = TrainingWeek.objects.get(id=week_id)
    week.completed = True
    week.save()
    return redirect('ngoma:training_week', week.id)


def training_weeks(request, macrocycle_id):
    macrocycle = ProfileMacrocycle.objects.get(id=macrocycle_id)
    weeks = TrainingWeek.objects.filter(macrocycle=macrocycle)

    context = {
        'macrocycle' : macrocycle,
        'weeks' : weeks
    }
    return render(request, 'training_weeks.html', context)

def training_week(request, week_id):
    week = TrainingWeek.objects.get(id=week_id)
    macrocycle = week.macrocycle
    profile = macrocycle.profile

    context = {
        'week' : week,
        'macrocycle' : macrocycle
    }
    return render(request, 'training_week.html', context)



def complete_session(request, attendance_id):
    session = Attendance.objects.get(id=attendance_id)
    session.completed = True
    session.save()
    return redirect('ngoma:profile_trainingblocks', session.macrocycle.id)

    
###  FORMS

from ngoma.forms import NewWorkoutDrillForm, NewSessionForm, NewMacrocycleForm, NewProfileMacrocycleForm, NewTestForm, NewTrainingThemeForm, NewTrainingBlockForm, NewMenuCategoryForm, NewMenuSubCategory, AttendanceForm


def forms_display(request):
    forms = Upload.objects.all()

    context = {
        'forms' : forms
    }
    return render(request, 'forms_display.html', context)


def new_athlete(request):
    if request.method == 'POST':
        form = NewAthleteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('ngoma:athletes')
    else:
        form = NewAthleteForm()

    return render(request, 'newathlete.html', {'form': form})

def edit_athlete(request, athlete_id):
    athlete = ProfileData.objects.get(id=athlete_id)

    if request.method != 'POST':
        form = NewAthleteForm(instance=athlete)

    else:
        form = NewAthleteForm(instance=athlete, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('ngoma:athlete', args=[athlete.id]))
            
    context = {
        'athlete' : athlete,
        'form' : form
    }
    return render(request, 'edit_athlete.html', context)
            
def new_workoutdrill(request, block_id):
    drill_block = BlockChoice.objects.get(id = block_id)
    if request.method == 'POST':
        form = NewWorkoutDrillForm(request.POST)
        if form.is_valid():
            drill = form.save(commit=False)
            drill.block = drill_block
            drill.save()
            return redirect('ngoma:workout_library')

    else:
        form = NewWorkoutDrillForm()


    context = {
        'drill_block' : drill_block,
        'form' : form
    }
    return render(request, 'new_workoutdrill.html', context)

def edit_workoutdrill(request, workoutdrill_id):
    workout_drill = WorkoutDrill.objects.get(id=workoutdrill_id)

    if request.method != 'POST':
        form = NewWorkoutDrillForm(instance=athlete)

    else:
        form = NewWorkoutDrillForm(instance=athlete, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('ngoma:workout_library'))

    context = {
        'workout_drill' : workout_drill,
        'form' : form
    }

    return render(request, 'edit_workoutdrill.html', context)
            
def new_session(request):
    if request.method == 'POST':
        form = NewSessionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ngoma:ngoma_dashboard')

    else:
        form = NewSessionForm()

    context = {
        
        'form' : form
    }

    return render(request, 'new_session.html', context)

def edit_session(request, session_id):
    session = Session.objects.get(id=session_id)

    if request.method != 'POST':
        form = NewSessionForm(instance=session)

    else:
        form = NewSessionForm(instance=session, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('ngoma:session', args=[session.id]))

    context = {
        'session' : session,
        'form' : form
    }
    return render(request, 'edit_session.html', context)
    
def new_macrocycle(request):
    if request.method == 'POST':
        form = NewMacrocycleForm(request.POST)
        if form.is_valid():
            form.save()

            
            return redirect('ngoma:ngoma_dashboard')

    else:
        form = NewMacrocycleForm()

    context = {
        
        'form' : form
    }

    return render(request, 'new_macrocycle.html', context)


def edit_macrocycle(request, macrocycle_id):
    macrocycle = Macrocycle.objects.get(id=macrocycle_id)

    if request.method != 'POST':
        form = NewMacrocycleForm(instance=macrocycle)

    else:
        form = NewMacrocycleForm(instance=macrocycle, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('ngoma:ngoma_dashboard'))

    context = {
        'macrocycle' : macrocycle,
        'form' : form
    }
    return render(request, 'edit_macrocycle.html', context)
    

def new_profilemacrocycle(request, athlete_id):
    def generate_training_weeks(profile_macrocycle):
            mc = profile_macrocycle  # Macrocycle object
        
            start = mc.start_date
            weeks = mc.macrocycle.estimated_weeks

            for week in range(1, int(weeks) + 1):
                TrainingWeek.objects.update_or_create(
                    macrocycle = profile_macrocycle,
                    week_number = week
                )
            
    athlete = ProfileData.objects.get(id=athlete_id)
    if request.method == 'POST':
        form = NewProfileMacrocycleForm(request.POST)
        
        if form.is_valid():
            macrocycle_form = form.save(commit=False)
            macrocycle_form.profile = athlete
            macrocycle_form.save()

            generate_training_weeks(macrocycle_form)
            
            return redirect('ngoma:athlete', athlete_id)

    else:
        form = NewProfileMacrocycleForm()

    context = {
        
        'form' : form,
        'athlete' : athlete
    }

    return render(request, 'new_profilemacrocycle.html', context)


def edit_profilemacrocycle(request, p_macrocycle_id):
    macrocycle = ProfileMacrocycle.objects.get(id = p_macrocycle_id)
    athlete = profile_macrocycle.profile
    if request.method != 'POST':
        form = NewProfileMacrocycleForm(instance=p_macrocycle)

    else:
        form = NewProfileMacrocycleForm(instance=macrocycle, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('ngoma:athlete', args=[athlete.id]))

    context = {
        'athlete' : athlete,
        'macrocycle' : macrocycle,
        'form' : form
    }
    return render(request, 'edit_profilemacrocycle.html', context)

    
def new_trainingtheme(request, macrocycle_id):
    macrocycle = ProfileMacrocycle.objects.get(id=macrocycle_id)
    profile = macrocycle.profile
    if request.method == 'POST':
        form = NewTrainingThemeForm(request.POST)
        if form.is_valid():
            trainingtheme_form = form.save(commit=False)
            trainingtheme_form.macrocycle = macrocycle
            trainingtheme_form.save()
            return redirect('ngoma:training_themes', macrocycle_id)

    else:
        form = NewTrainingThemeForm()

    context = {
        'profile' : profile,
        'form' : form,
        'macrocycle' : macrocycle
    }

    return render(request, 'new_trainingtheme.html', context)


def edit_trainingtheme(request, theme_id):
    theme = TrainingTheme.objects.get(id=theme_id)
    if request.method != 'POST':
        form = NewTrainingThemeForm(instance=theme)

    else:
        form = NewTrainingThemeForm(instance=theme, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('ngoma:training_theme', args=[theme.id]))

    context = {
        'theme' : theme,
        'form' : form
    }
    return render(request, 'edit_trainingtheme.html', context)


def new_trainingblock(request, theme_id):
    theme = TrainingTheme.objects.get(id=theme_id)
    profile = theme.profile
    if request.method == 'POST':
        form = NewTrainingBlockForm(request.POST)
        if form.is_valid():
            trainingblock_form = form.save(commit=False)
            trainingblock_form.theme = theme
            trainingblock_form.save()
            return redirect('ngoma:profile_trainingthemes', profile.id)

    else:
        form = NewTrainingBlockForm()

    context = {
        
        'form' : form,
        'theme' : theme
        
    }

    return render(request, 'new_trainingblock.html', context)


def edit_trainingblock(request, block_id):
    block = TrainingBlock.objects.get(id=block_id)
    if request.method != 'POST':
        form = NewTrainingBlockForm(instance=block)

    else:
        form = NewTrainingBlockForm(instance=block, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('ngoma:training_block', block_id))

    context = {
        'block' : block,
        'form' : form
    }
    return render(request, 'edit_trainingtheme.html', context)

    
def new_testname(request):
    if request.method == 'POST':
        form = NewTestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ngoma:tests_display')

    else:
        form = NewTestForm()

    context = {
        
        'form' : form
    }

    return render(request, 'new_testname.html', context)


def edit_testname(request, test_id):
    test = TestName.objects.get(id=test_id)
    if request.method != 'POST':
        form = NewTestForm(instance=test)

    else:
        form = NewTestForm(instance=test, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('ngoma:test_display', args=[test.id]))

    context = {
        'test' : test,
        'form' : form
    }
    return render(request, 'edit_testname.html', context)

def new_attendance(request, profilemacrocycle_id):
    profile_macrocycle = ProfileMacrocycle.objects.get(id=profilemacrocycle_id)

    if request.method == 'POST':
        form = AttendanceForm(request.POST, profile_macrocycle=profile_macrocycle)
        if form.is_valid():
            attendance = form.save(commit=False)
            attendance.profile = profile_macrocycle
            attendance.save()
            return redirect('ngoma:profile_trainingblock', profilemacrocycle_id)

    else:
        form = AttendanceForm(profile_macrocycle=profile_macrocycle)

    context = {
        'profile_macrocycle' : profile_macrocycle,
        'form' : form
    }
    return render(request, 'new_attendance.html', {'form': form})

def edit_attendance(request, attendance_id):
    attendance = Attendance.objects.get(id=attendance_id)
    macrocycle = attendance.profile
    if request.method != 'POST':
        form = AttendanceForm(instance=attendance)

    else:
        form = AttendanceForm(instance=attendance, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpsResponseRedirect(reverse('ngoma:profile_trainingblock', macrocycle.id))

    context = {
        'attendance' : attendance,
        'macrocycle' : macrocycle,
        'form' : form
    }

    return render(request, 'edit_attendance.html', context)


