from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo = models.ImageField(upload_to='images/', blank=True)
    bio = models.TextField(blank=True)
    gender = models.CharField(max_length=1, choices=(
        ('M', 'Male'), ('F', 'Female'), ('O', 'Other')), blank=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    phone = models.PositiveIntegerField(blank=True)

    def __str__(self):
        return self.user

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
        db_table = 'userprofile'


class Location(models.Model):
    location = models.CharField(max_length=50)

    def save_location(self):
        self.save()

    def __str__(self):
        return self.location


class tag(models.Model):
    tag = models.CharField(max_length=100)

    def save_tag(self):
        self.save()


class Photo(models.Model):
    photo = models.ImageField(upload_to='images/')
    caption = models.TextField(blank=True)
    location = models.ManyToManyField(Location, blank=True)
    likes = models.IntegerField(blank=True)


class Comment(models.Model):
    photo = models.IntegerField(Photo)
    pass
