from django.urls import path

from . import views

app_name = 'Platform1'
urlpatterns=[
    #Home Page
    path('', views.index, name='index'),

    #Newsletters page
    path('newsletters/', views.newsletters, name='newsletters'),

    #Newsletter page
    path('newsletters/<int:newsletter_id>/', views.newsletters, name='newsletters'),

    #Calendar
    path('calendar/', views.calendar, name='calendar'),

    #Directory
    path('directory/', views.directory, name='directory'),

    #Resource board page
    path('resource_board/', views.resource_board, name='resource_board'),

    #Media galleries page
    path('media_galleries/', views.media_galleries, name='media_galleries'),

    #Sponsors page
    path('sponsors/', views.sponsors, name='sponsors'),
    
    #Forms page
    path('registration_forms/', views.registration_forms, name='registration_forms'),
    
    #Contacts page
    path('contacts/', views.contacts, name='contacts'),
    
    #Admin Dashboard page
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard')
]