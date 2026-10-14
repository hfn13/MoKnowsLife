from django.urls import path

from . import views

app_name = 'ngoma'

urlpatterns=[
    # Home Page
    path('ngoma_index/', views.ngoma_index, name='ngoma_index'),

    path('events/<str:date>/', views.events_for_date, name='events_for_date'),

    ### DASHBOARDS
    
    # List of Athletes
    path('athletes/', views.athletes, name='athletes'),

    # Athlete dashboard
    path('athletes/<int:athlete_id>/', views.athlete, name='athlete'),

    # Admin / Coach Dashboard
    path('ngoma_dashboard/', views.ngoma_dashboard, name='ngoma_dashboard'),

    # Macrocycles page
    path('macrocycles/', views.macrocycles, name='macrocycles'),

    # Macrocycle page
    path('macrocycle/<int:macrocycle_id>', views.macrocycle, name='macrocycle'),

    # Sessions Page
    path('sessions/', views.sessions, name='sessions'),

    # Session Page
    path('sessions/<int:session_id>/', views.session, name='session'),

    # Training themes page
    path('training_themes/', views.training_themes, name='training_themes'),

    # Training theme page
    path('training_theme/<int:theme_id>/', views.training_theme, name='training_theme'),

    # Training blocks
    path('training_blocks/', views.training_blocks, name='training_blocks'),

    # Training block
    path('training_block/<int:block_id>/', views.training_block, name='training_block'),

    # Profile training themes
    path('profile_trainingthemes/<int:profile_id>/', views.profile_trainingthemes, name='profile_trainingthemes'),

    #Profile training blocks
    path('profile_trainingblocks/<int:theme_id>/', views.profile_trainingblocks, name='profile_trainingblocks'),

    # Complete week button
    path('complete_week/<int:week_id>/', views.complete_week, name='complete_week'),

    # Complete session button
    path('complete_session/<int:attendance_id>', views.complete_session, name='complete_session'),

    # Training Weeks
    path('training_weeks/<int:macrocycle_id>', views.training_weeks, name='training_weeks'),

    #Training Week
    path('training_week/<int:week>/', views.training_week, name='training_week'),

    ### WORKOUT PAGES
    
    #Workout library
    path('workout_library/', views.workout_library, name='workout_library'),

    #Phase view
    path('phase_view/<int:phase_id>/', views.phase_view, name='phase_view'),

    #Phase view
    path('block_view/<int:block_id>/', views.block_view, name='block_view'),
    
    #Menu Library
    path('menu_library/', views.menu_library, name='menu_library'),

    #Menu
    path('menu_category/<int:cat_id>/', views.menucategory, name='menu_category'),

    #Update menus
    path('update_menus/', views.update_menuoptions, name='update_menu'),

    #Sub Menu
    path('menu_subcategory/<int:subcat_id>/', views.menusubcategory, name='menu_subcategory'),

    #Update Sub Menu
    path('update_submenu/<int:submenu_id>/', views.update_submenu, name='update_submenu'),

    #Upload success
    path('upload_success/', views.upload_success, name='upload_success'),

    
    # Update athlete data
    # path('update_athlete_profile/<int:athlete_id>/', views.update_athlete_profile, name='update_athlete_profile'),

    

    ### FORMS
    #Upload forms
    path('upload/', views.upload_file, name='upload'),
    
    # Consent Forms
    path('consent_forms/', views.forms_display, name='forms_display'),

    # Add new athlete
    path('add_athlete/', views.new_athlete, name='add_athlete'),

    # Edit athlete form
    path('edit_athlete/<int:athlete_id>/', views.edit_athlete, name='edit_athlete'),

    # Add new workoutdrill
    path('add_workoutdrill/<int:block_id>/', views.new_workoutdrill, name='add_workoutdrill'),

    # Edit workoutdrill
    path('edit_workoutdrill/<int:workoutdrill_id>/', views.edit_workoutdrill, name='edit_workoutdrill'),

    # Add new session
    path('add_newsession/', views.new_session, name='new_session'),

    # Edit session
    path('edit_session/<int:session_id>/', views.edit_session, name='edit_session'),

    # Add new macrocycle
    path('add_macrocycle/', views.new_macrocycle, name='new_macrocycle'),

    # Edit macrocycle
    path('edit_macrocycle/<int:macrocycle_id>/', views.edit_macrocycle, name='edit_macrocycle'),

    # Add new profile macrocycle
    path('add_profilemacrocycle/<int:athlete_id>/', views.new_profilemacrocycle, name='new_profilemacrocycle'),

    # Edit profile macrocycle
    path('edit_profilemacrocycle/<int:p_macrocycle_id>/', views.edit_profilemacrocycle, name='edit_profilemacrocycle'),

    # Add new training theme
    path('add_trainingtheme/<int:macrocycle_id>/', views.new_trainingtheme, name='new_trainingtheme'),

    # Edit training theme
    path('edit_trainingtheme/<int:theme_id>/', views.edit_trainingtheme, name='edit_trainingtheme'),

    # Add new training block
    path('add_trainingblock/<int:theme_id>/', views.new_trainingblock, name='new_trainingblock'),

    # Edit training block
    path('edit_trainingblock/<int:block_id>/', views.edit_trainingblock, name='edit_trainingblock'),

    # Add new Test
    path('add_testname/', views.new_testname, name='new_testname'),

    # Edit Test
    path('edit_testname/<int:test_id>/', views.edit_testname, name='edit_testname'),

    # New Attendance
    path('add_attendance/<int:macrocycle_id>/', views.new_attendance, name='new_attendance'),

    # Edit attendance
    path('edit_attendance/<int:attendance_id>/', views.edit_attendance, name='edit_attendance')
]