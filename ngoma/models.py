from django.db import models

# Create your models here.
## ATHLETE MODELS
class ClientCategory(models.Model):
    category = models.CharField(max_length=200)
    def __str__(self):
        return self.category

    class Meta:
        verbose_name_plural = 'Client categories'
        
class WorkoutCategory(models.Model):
    category = models.CharField(max_length=200)

    def __str__(self):
        return self.category

    class Meta:
        verbose_name_plural = 'Workout categories'

class Status(models.Model):
    status = models.CharField(max_length=200)

    def __str__(self):
        return self.status

    class Meta:
        verbose_name_plural = 'Status'

  

## LAYER MODELS
class Macrocycle(models.Model):
    name = models.CharField(max_length=200)
    start_date = models.DateField(null=True, blank=True)
    estimated_weeks = models.IntegerField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    #athlete = models.ForeignKey(ProfileData, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class SeasonPhase(models.Model):
    
    phase = models.CharField(max_length=200)
    code = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.code

        
## WORKOUT MODELS

class PhaseChoice(models.Model):
    
    phase = models.CharField(max_length=200)
    order = models.IntegerField()
    description = models.TextField(blank=True)
    
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
    sets = models.IntegerField(blank=True, null=True)
    repetitions = models.IntegerField(blank=True, null=True)
    distance = models.IntegerField(blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    prescription = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    
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

    class Meta:
        verbose_name_plural = 'Menu Categories'

        
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

    class Meta:
        verbose_name_plural = 'Menu SubCategories'


class Session(models.Model):
    
    name = models.CharField(max_length=200)
    session_type = models.ManyToManyField(WorkoutCategory)
    menu_type = models.ManyToManyField(MenuCategory)
    date = models.DateTimeField()
    location = models.CharField(max_length=100, blank=True)
    drills = models.ManyToManyField(WorkoutDrill, blank=True)

    def __str__(self):
        return f'{self.name} at {self.location}'

    class Meta:
        app_label='ngoma'


class ProfileData(models.Model):
    
    first_name = models.CharField(max_length=200)
    middle_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200)
    DOB = models.DateField(blank=True, null=True)
    height = models.DecimalField(blank=True, null=True, max_digits=6, decimal_places=2)
    weight = models.DecimalField(blank=True, null=True, max_digits=6, decimal_places=2)
    client_category = models.ForeignKey(ClientCategory, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to=None, blank=True, null=True)

    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    
    class Meta:
        app_label='ngoma'

    class Meta:
        verbose_name_plural = 'Profile Data'


class ProfileMacrocycle(models.Model):
    AVAILABILITY_CHOICES = [
        ('available', 'AVAILABILITY'),
        ('unavailable', 'UNAVAILABLE'),
        ('injured', 'INJURED')
    ]
    
    macrocycle = models.ForeignKey(Macrocycle, on_delete=models.CASCADE)
    profile = models.ForeignKey(ProfileData, on_delete=models.CASCADE)
    season_phase = models.ForeignKey(SeasonPhase, on_delete=models.SET_NULL, null=True, blank=True)
    program_phase = models.ForeignKey(PhaseChoice, on_delete=models.SET_NULL, null=True, blank=True)
    availability = models.CharField(choices = AVAILABILITY_CHOICES, default='available')
    
    def __str__(self):
        return f'{self.profile.last_name} - {self.macrocycle}'      

class TrainingWeek(models.Model):
    
    macrocycle = models.ForeignKey(ProfileMacrocycle, on_delete=models.CASCADE)
    week_number = models.IntegerField()

    def __str__(self):
        return f'Week {self.week_number}'
        
class TrainingTheme(models.Model):
    
    macrocycle = models.ForeignKey(ProfileMacrocycle, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    start_week = models.ForeignKey(TrainingWeek, on_delete=models.CASCADE, null=True, blank=True, related_name='trainingtheme_start_weeks')
    end_week = models.ForeignKey(TrainingWeek, on_delete=models.CASCADE, null=True, blank=True, related_name='trainingtheme_end_weeks')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.theme



 

class TrainingBlock(models.Model):

    name =  models.CharField(max_length=200)
    theme = models.ForeignKey(TrainingTheme, on_delete=models.CASCADE)
    start_week =  models.ForeignKey(TrainingWeek, on_delete=models.CASCADE, null=True, blank=True, related_name='trainingblock_start_weeks')
    end_week =  models.ForeignKey(TrainingWeek, on_delete=models.CASCADE, null=True, blank=True, related_name='trainingblock_end_weeks')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.block


class Attendance(models.Model):
   
    player = models.ForeignKey(ProfileData, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('player', 'session')

    class Meta:
        app_label='ngoma'

###

class TestQuality(models.Model):
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class TestName(models.Model):
    
    name = models.CharField(max_length=200)
    quality = models.ForeignKey(TestQuality, on_delete=models.SET_NULL, null=True, blank=True)
    protocol = models.CharField(blank=True, null=True)
    unit = models.CharField(blank=True, null=True)
    direction = models.CharField(blank=True, null=True)
    attempts = models.CharField(blank=True, null=True)
    equipment = models.CharField(blank=True, null=True)
    classification = models.CharField(blank=True, null=True)

    def __str__(self):
        return self.name

class TrackTest(models.Model):
    
    CLASSIFICATION_CHOICES = [
        ('UNIVERSAL', 'Universal'),
        ('OPTIONAL', 'Optional'),
        ('SPORT-SPECIFIC', 'Sport-specific')
    ]
    test = models.ForeignKey(TestName, on_delete=models.CASCADE)
    classification = models.CharField(choices = CLASSIFICATION_CHOICES)
    
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

    class Meta:
        verbose_name_plural = 'Track Test Data'

class LiftTest(models.Model):

    CLASSIFICATION_CHOICES = [
        ('UNIVERSAL', 'Universal'),
        ('OPTIONAL', 'Optional'),
        ('SPORT-SPECIFIC', 'Sport-specific')
    ]
    test = models.ForeignKey(TestName, on_delete=models.CASCADE)
    classification = models.CharField(choices = CLASSIFICATION_CHOICES)
    
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

    class Meta:
        verbose_name_plural = 'Lift Test Data'


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

    class Meta:
        verbose_name_plural = 'Trend Analyses'


class TrendTest(models.Model):
    
    CLASSIFICATION_CHOICES = [
        ('UNIVERSAL', 'Universal'),
        ('OPTIONAL', 'Optional'),
        ('SPORT-SPECIFIC', 'Sport-specific')
    ]
    
    test = models.ForeignKey(TestName, on_delete=models.CASCADE)
    classification = models.CharField(choices = CLASSIFICATION_CHOICES)
    
    def __str__(self):
        return self.test


class TrendTestData(models.Model):

    profile = models.ForeignKey(ProfileData, on_delete=models.CASCADE)
    analyses = models.ForeignKey(TrendAnalyses, on_delete=models.SET_NULL, null=True, blank=True)
    test = models.ForeignKey(TestName, on_delete=models.CASCADE)
    date = models.DateField()
    value = models.DecimalField(max_digits=6, decimal_places=2)
    
    def __str__(self):
        return f'{self.profile} {self.test}'


class CISTIScore(models.Model):
    
    CHOICES = [
        ('C', 'Consistency'),
        ('IN', 'Intensity'),
        ('S', 'Speed'),
        ('T', 'Technique'),
        ('I', 'Intent'),
        ('Overall', 'Overall')
    ]
    test = models.ForeignKey(TrendTestData, on_delete=models.CASCADE)
    metric = models.CharField(choices=CHOICES)
    score = models.DecimalField(max_digits=6, decimal_places=2)
    notes = models.TextField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'{self.test} - {self.metric}'

class Upload(models.Model):
    
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='uploads/')

    def __str__(self):
        return self.title

    class Meta:
        app_label='ngoma'