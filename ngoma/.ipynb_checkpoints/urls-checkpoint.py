from django.urls import path

from . import views

app_name = 'ngoma'

urlpatterns=[
    # Home Page
    path('ngoma_index/', views.ngoma_home, name='ngoma_home'),

    # List of Athletes
    path('athletes/', views.athletes, name='athletes'),

    #Athlete dashboard
    path('athletes/<int:athlete_id>/', views.athlete, name='athlete'),

    #Forms
    path('consent_forms/', views.forms_display, name='forms_display'),

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

    #Upload forms
    path('upload/', views.upload_file, name='upload'),

    #Upload success
    path('upload_success/', views.upload_success, name='upload_success'),

    #Athletes
    path('athletes/', views.athletes, name = 'athletes'),

    #Athlete dashboard
    path('athletes/<int:athlete_id>/', views.athlete, name='athlete'),

    #Add new athlete
    path('add_athlete/', views.new_athlete, name='add_athlete'),

    # Update athlete data
    path('update_athlete_profile/<int:athlete_id>/', views.update_athlete_profile, name='update_athlete_profile')
   
]