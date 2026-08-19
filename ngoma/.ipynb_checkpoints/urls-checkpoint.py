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

    #Upload forms
    path('upload/', views.upload_file, name='upload'),

    #Upload success
    path('upload_success/', views.upload_success, name='upload_success'),

    #Update menus
    path('update_menus/', views.update_menuoptions, name='update_menu')
]