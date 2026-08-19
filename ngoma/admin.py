from django.contrib import admin

from .models import ProfileData,Session,Attendance,TrackTest,TrackTestData,LiftTest,LiftTestData,WorkoutDrill,Upload,MenuCategory,MenuSubCategory

# Register your models here.
admin.site.register(ProfileData)
admin.site.register(Session)
admin.site.register(MenuCategory)
admin.site.register(MenuSubCategory)
admin.site.register(Attendance)
admin.site.register(TrackTest)
admin.site.register(TrackTestData)
admin.site.register(LiftTest)
admin.site.register(LiftTestData)
admin.site.register(WorkoutDrill)
admin.site.register(Upload)