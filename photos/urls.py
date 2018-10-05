from django.conf.urls import url
from . import views

urlpatterns = [
    url('^$', views.home, name='home'),
    url('^register/$', views.signup, name='signup'),
    url('^new/post/$', views.new_post, name='new_post'),
]
