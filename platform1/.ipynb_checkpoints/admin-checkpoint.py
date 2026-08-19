from django.contrib import admin
from platform1.models import Organisation, NewsLetter, Article, Media, Staff
# Register your models here.


admin.site.register(Organisation)
admin.site.register(NewsLetter)
admin.site.register(Article)
admin.site.register(Media)
admin.site.register(Staff)