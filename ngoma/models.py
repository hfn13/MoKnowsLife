from django.db import models

# Create your models here.
class ProfileData(models.Model):
    first_name = models.CharField(max_length=200)
    middle_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200)
    DOB = models.DateField(blank=True, null=True)
    height = models.DecimalField(blank=True, null=True, max_digits=6, decimal_places=2)
    weight = models.DecimalField(blank=True, null=True, max_digits=6, decimal_places=2)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        app_label='ngoma'

class PhaseChoice(models.Model):
    phase = models.CharField(max_length=200)
    order = models.IntegerField()
    
    def __str__(self):
        return self.phase

    class Meta:
        app_label='ngoma'

class BlockChoice(models.Model):
    phase = models.ForeignKey(PhaseChoice, on_delete=models.CASCADE)
    block = models.CharField(max_length=200)
    def __str__(self):
        return f'{self.block} {self.phase.order}'

    class Meta:
        app_label='ngoma'
        
class WorkoutDrill(models.Model):

    block = models.ForeignKey(BlockChoice,  on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    sets = models.IntegerField(blank=True)
    repetitions = models.IntegerField(blank=True)
    distance = models.IntegerField(blank=True)
    duration = models.IntegerField(blank=True)
    prescription = models.CharField(max_length=200)
    def __str__(self):
        return f'{self.name}'

    class Meta:
        app_label='ngoma'

class MenuCategory(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=200)         
    description = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    def __str__(self):
        return f'Menu {self.code}: {self.name}'

    class Meta:
        app_label='ngoma'

class MenuSubCategory(models.Model):
    category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE)
    code = models.CharField(max_length=10, unique=True)
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True, null=True) 
    best_for = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.code} — {self.title}"

    class Meta:
        app_label='ngoma'


class Session(models.Model): 
    session_type = models.ForeignKey(MenuCategory, null=True, on_delete=models.SET_NULL)
    date = models.DateField()
    time = models.TimeField(null=True,blank=True)
    location = models.CharField(max_length=100, blank=True)
    #drills = models.ManyToManyField(TrainingDrill, blank=True)

    def __str__(self):
        return f'{self.date} {self.session_type} at {self.location}'

    class Meta:
        app_label='ngoma'

class Attendance(models.Model):
   
    player = models.ForeignKey(ProfileData, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)

    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ('player', 'session')

    class Meta:
        app_label='ngoma'

class TrackTest(models.Model):
    
    test = models.CharField(max_length=200)

    def __str__(self):
        return self.test

    class Meta:
        app_label='ngoma'

# class TrackTestProfile(models.Model):
#     athlete = models.ForeignKey(ProfileData, on_delete=models.CASCADE)
#     test = models.ForeignKey(TrackTest, on_delete=models.CASCADE)
     

class TrackTestData(models.Model):

    profile = models.ForeignKey(ProfileData, on_delete = models.CASCADE)
    test = models.ForeignKey(TrackTest, on_delete=models.CASCADE)
    date = models.DateTimeField()
    value = models.DecimalField(blank=True, null=True, max_digits=6, decimal_places=2)

    class Meta:
        app_label='ngoma'

class LiftTest(models.Model):

    test = models.CharField(max_length=200)

    def __str__(self):
        return self.test

    class Meta:
        app_label='ngoma'


class LiftTestData(models.Model):
    profile = models.ForeignKey(ProfileData, on_delete = models.CASCADE)
    test = models.ForeignKey(LiftTest, on_delete=models.CASCADE)
    date = models.DateTimeField(blank=True, null=True)
    value = models.DecimalField(blank=True, null=True, max_digits=6, decimal_places=2)

    class Meta:
        app_label='ngoma'

class MenuOption(models.Model):
    category = models.ForeignKey(MenuSubCategory, on_delete=models.CASCADE)
    block = models.CharField()

    def __str__(self):
        return self.block

    class Meta:
        app_label='ngoma'

class TrendAnalyses(models.Model):
    analyses = models.CharField(max_length=200)

    def __str__(self):
        return self.analyses

class TrendTest(models.Model):
    test = models.CharField(max_length=200)

    def __str__(self):
        return self.test

class TrendTestData(models.Model):

    profile = models.ForeignKey(ProfileData, on_delete=models.CASCADE)
    analyses = models.ForeignKey(TrendAnalyses, on_delete=models.SET_NULL, null=True, blank=True)
    test = models.ForeignKey(TrendTest, on_delete=models.CASCADE)
    date = models.DateField(blank=True, null=True)
    value = models.DecimalField(max_digits=6, decimal_places=2)
    
    
    def __str__(self):
        return f'{self.profile} {self.test}'


class CISTI_score(models.Model):
    test = models.OneToOneField(TrendTest, on_delete=models.SET_NULL, null=True)
    consistency = models.DecimalField(max_digits=6, decimal_places=2)
    intensity = models.DecimalField(max_digits=6, decimal_places=2)
    speed = models.DecimalField(max_digits=6, decimal_places=2)
    technique = models.DecimalField(max_digits=6, decimal_places=2)
    intent = models.DecimalField(max_digits=6, decimal_places=2)
    overall = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'CISTI score: {self.overall}'


class Upload(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='uploads/')

    def __str__(self):
        return self.title

    class Meta:
        app_label='ngoma'