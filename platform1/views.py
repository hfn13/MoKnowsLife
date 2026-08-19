from django.shortcuts import render
from platform1.models import Organisation, NewsLetter, Article, Media, Staff
from django.utils import timezone



# Create your views here.
def index(request):
    'Home page.'
    return render(request,'index.html')

def news(request):
    'Main news articles displayed here.'
    newsletter = NewsLetter.objects.filter()
    return render(request, 'news.html')

def calendar(request):
    'Page with calendar.'

    return render(request, 'calendar.html')

def newsletters(request):
    'List of all newsletters that have been published.'
    newsletters = NewsLetter.objects.all()
    
    context = {
        'newsletters' : newsletters
    }
    return render(request, 'newsletter.html', context)

def newsletter(request, newsletter_id):
    'Articles published on the same day grouped together.'
    newsletter = NewsLetter.objects.order_by('-date').first()
    articles = Article.objects.filter(newsletter=newsletter)
    context = {
        'newsletter' : newsletter,
        'articles' : articles
    }
    
    return render(request, 'newsletter.html', context)

def directory(request):
    'List of individuals involved with the organisation.'
    staff = Staff.objects.all()

    context = {
        'staff' : staff
    }
    
    return render(request, 'directory.html', context)

def resource_board(request):
    
    return render(request, 'resource_board.html')

def media_galleries(request):
    'List of all media galleries.'
    return render(request, 'media_galleries.html')

def media_gallery(request):
    'Page showing selected media gallery.'
    'Organized according to events.'
    return render(request, 'media_gallery.html')

def sponsors(request):
    'List of sponsors.'
    return render(request, 'sponsors.html')

def registration_forms(request):
    'Page enabling registration of new clients.'
    return render(request, 'registration_forms.html')

def contacts(request, organisation_id):
    'Page with organisation contact details.'
    organisation = Organisation.objects.get(id = organisation_id)

    context = {
        'organisation' : organisation
    }
    return render(request, 'contacts.html', context)

def admin_dashboard(request):
    'Administrators dashboard.'
    return render(request, 'admin_dashboard.html')

