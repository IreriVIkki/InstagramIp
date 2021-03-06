from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url('^$', views.home, name='home'),
    url('^register/$', views.signup, name='signup'),
    url('^new/post/$', views.new_post, name='new_post'),
    url('^edit/profile/$', views.edit_profile, name='edit_profile'),
    url('^query/profile/(\w+)$', views.other_profile, name='other_profile'),
    url('^user/profile/$', views.profile, name='profile'),
    url('^search/photos/$', views.search_results, name='search'),
    url('^discover/photos/and/people/$', views.explore, name='explore'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
