from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, null=True, related_name='profile')
    change_profile_photo = models.ImageField(
        upload_to='images/', blank=True,)
    name = models.CharField(max_length=50)
    user_name = models.CharField(max_length=50, null=True)
    bio = models.TextField(blank=True)
    website = models.CharField(max_length=150, null=True)
    STATUS_CHOICES = (
        ('Male', ("Male")),
        ('Female', ("Female")),
        ('Other', ("Other")),
    )
    gender = models.CharField(
        max_length=20, choices=STATUS_CHOICES, blank=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    phone = models.PositiveIntegerField(null=True)
    email = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.user_name

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
    uploaded_by = models.ForeignKey(User, null=True, related_name='photos')
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

    @classmethod
    def filter_by_search_term(cls, search_term):
        return cls.objects.filter(caption__icontains=search_term)

    def get_user_profile(self, photo):
        photos = Photo.objects.filter(uploaded_by=photo.uploaded_by)
        return photos

    def save_photo(self, user):
        self.uploaded_by = user
        self.save()

    def __str__(self):
        return self.caption


class Comment(models.Model):
    author = models.ForeignKey(User, related_name='comments', null=True)
    photo = models.ForeignKey(Photo, related_name='comments', null=True)
    comment = models.CharField(max_length=1000)
    posted_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment

    @classmethod
    def all_photo_comments(cls, photo_id):
        ph = Photo.objects.get(pk=photo_id)
        comments = Comment.objects.filter(photo=ph)
        return comments

    def save_comment(self, user, photo):
        self.author = user
        self.photo = photo
        self.save()


class PhotoLikes(models.Model):
    photo = models.ForeignKey(Photo, related_name='likes', null=True)
    liked_by = models.ForeignKey(User, related_name='liked_photos', null=True)

    def save_like(self, photo, user):
        self.photo = photo
        self.liked_by = user
        self.save()


class CommentLikes(models.Model):
    photo = models.ForeignKey(Comment, related_name='likes')
    likes = models.ForeignKey(User, related_name='liked_comments')


class UserFavourites(models.Model):
    user = models.ForeignKey(User, related_name='saved')
    photo = models.ForeignKey(Photo, related_name='favourites')


class Followers(models.Model):
    follower = models.ForeignKey(User, related_name='followers', null=True)
    following = models.ForeignKey(User, related_name='following', null=True)
    followed_on = models.DateTimeField(auto_now_add=True)

    def follow_user(self, current_user, user_other):
        self.following = user_other
        self.follower = current_user
        self.save()

    def unfollow_user(self, user):
        fol = Followers.objects.get(follower=user)
        fol.delete()

    def __str__(self):
        return f'{self.follower.username} is now following {self.following.username}'
