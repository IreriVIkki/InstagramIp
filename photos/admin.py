from django.contrib import admin
from .models import UserProfile, Location, tags, Photos
# Register your models here.


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio', 'gender', 'phone']


class PhotosAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(tags)
admin.site.register(Location)
admin.site.register(Photos)
