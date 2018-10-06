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
    uploaded_by = models.ForeignKey(User, null=True)
    photo = models.ImageField(upload_to='images/')
    caption = models.TextField(blank=True)
    location = models.ManyToManyField(Location, blank=True)
    post_date = models.DateTimeField(auto_now_add=True)

    @classmethod
    def all_photos(cls):
        all_photos = cls.objects.all()
        return all_photos

    @classmethod
    def user_photos(cls, user_name):
        user = User.objects.filter(username=user_name)[0]
        photos = cls.objects.filter(uploaded_by=user)
        return photos

    def __str__(self):
        return self.caption


class Comment(models.Model):
    author = models.ForeignKey(User, related_name='comments')
    photo = models.ForeignKey(Photo, related_name='comments')
    comment = models.TextField(blank=True)
    posted_date = models.DateTimeField(auto_now_add=True)


class PhotoLikes(models.Model):
    photo = models.ForeignKey(Photo, related_name='likes')
    liked_by = models.ForeignKey(User, related_name='liked_photos')


class CommentLikes(models.Model):
    photo = models.ForeignKey(Comment, related_name='likes')
    likes = models.ForeignKey(User, related_name='liked_comments')


class UserFavourites(models.Model):
    user = models.ForeignKey(User, related_name='saved')
    photo = models.ForeignKey(Photo, related_name='favourites')
