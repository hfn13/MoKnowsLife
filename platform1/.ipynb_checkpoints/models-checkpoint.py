from django.db import models

# Create your models here.
class Organisation(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField()
    phone = models.IntegerField(blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.name
    

class NewsLetter(models.Model):
    date = models.DateField()

    def __str__(self):
        return self.date

class Article(models.Model):
    newsletter = models.ForeignKey(NewsLetter, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    entry = models.TextField()

    def __str__(self):
        return self.titles

class Media(models.Model):
    image = models.ImageField()
    event = models.CharField()

class Staff(models.Model):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(blank=True)
    last_name = models.CharField(max_length=50)
    dateofbirth = models.DateField()
    group = models.ForeignKey(Organisation,null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.first_name + ' ' + self.last_name