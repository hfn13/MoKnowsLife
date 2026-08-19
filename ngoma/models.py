from django.db import models

# Create your models here.
class ProfileData(models.Model):
    first_name = models.CharField(max_length=200)
    middle_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200)
    DOB = models.DateField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.first_name + self.last_name

class MenuCategory(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=200)         
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Menu {self.code}'

class MenuSubCategory(models.Model):
    category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE)
    code = models.CharField(max_length=10, unique=True)
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True, null=True)  
    best_for = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.code} — {self.title}"


class Session(models.Model):
    
    session_type = models.ForeignKey(MenuCategory, null=True, on_delete=models.SET_NULL)
    date = models.DateField()
    time = models.TimeField(null=True,blank=True)
    location = models.CharField(max_length=100, blank=True)
    #drills = models.ManyToManyField(TrainingDrill, blank=True)

    def __str__(self):
        return f'{self.date} {self.session_type} at {self.location}'

class Attendance(models.Model):
   
    player = models.ForeignKey(ProfileData, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)

    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ('player', 'session')

class TrackTest(models.Model):
    TRACK_TESTS = [
        ('100M','100m'),
         ('200M','200m'),
         ('VERTICAL','Vert (in)'),
         ('SINGLE LEG HOLD RIGHT','SL Hld R (s)'),
         ('SINGLE HOLD LEFT','SL Hld L (s)'),
         ('SINGLE LEG BOUND','SL Bound (s)'),
         ('CORE','Core (reps)'),
         ('FLY ZONE','Fly Zone (s)'),
         ('SPRINT MOBILITY','Sprint Mobility'),
         ('AGILITY','Agility')
    ]
    test = models.CharField(max_length=200, choices=TRACK_TESTS)

class TrackTestData(models.Model):

    profile = models.ForeignKey(ProfileData, on_delete = models.CASCADE)
    test = models.OneToOneField(TrackTest, on_delete=models.CASCADE)
    date = models.DateTimeField()
    time = models.IntegerField(blank=True, null=True)
    
    

class LiftTest(models.Model):
    LIFT_TESTS = [
        ('LIFT AND JERK','LJ'),
        ('OVERHEAD THROW','OVHD Thr (m)'),
        ('CHEST THROW','CHST Thr (m)'),
        ('OVERHEAD SQUAT','OVHD SQT'),
        ('LUNGE MATRIX','Lunge MTRX'),
        ('PUSH UP HOLD HIGH','Push up Hld H (s)'),
        ('PUSH UP HOLD LOW','Push up Hld L (s)'),
        ('PUSH UP REPS','Push up Reps'),
        ('SQUAT','SQT (reps)'),
        ('WALL SIT','Wall Sit (s)'),
        ('DEAD HANG','Dead Hang (s)'),
        ('ISOMETRIC HOLD RIGHT','ISO Hld R (s)'),
        ('ISOMETRIC HOLD LEFT','ISO Hld L (s)')
    ]

    test = models.CharField(max_length=200, choices=LIFT_TESTS)

class LiftTestData(models.Model):
    profile = models.ForeignKey(ProfileData, on_delete = models.CASCADE)
    test = models.OneToOneField(LiftTest, on_delete=models.CASCADE)
    date = models.DateTimeField(blank=True, null=True)
    time = models.IntegerField(blank=True, null=True)

class WorkoutDrill(models.Model):
    phase_choices = [
        ('base', 'Base'),
        ('buid', 'Build'),
        ('peak', 'Peak')
    ]

    workout_choices = [
         ('warm up', 'Warm up'),
         ('mobility', 'Mobility'),
         ('cool down', 'Cool Down'),
         ('hips', 'Hips'),
         ('core', 'Core'),
         ('med ball', 'Med Ball'),
         ('sled', 'Sled'),
         ('plyo', 'Plyo'),
         ('posture', 'Posture'),
         ('sprint reaction', 'Sprint Reaction'),
         ('wall drills', 'Wall Drills')
    ]

    menu = models.ManyToManyField(MenuSubCategory, blank=True)
    order = models.IntegerField()
    name = models.CharField(max_length=200)
    sets = models.IntegerField(blank=True)
    repetitions = models.IntegerField(blank=True)
    distance = models.IntegerField(blank=True)
    duration = models.IntegerField(blank=True)
    phase = models.CharField(choices=phase_choices, blank=True)
    workout = models.CharField(choices=workout_choices, blank=True)
    
    def __str__(self):
        return self.name


class Upload(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='uploads/')

    def __str__(self):
        return self.title