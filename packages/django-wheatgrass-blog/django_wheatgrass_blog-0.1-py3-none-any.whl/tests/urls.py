'''Custom URL configuration for testing.'''

from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    # Main URL configuration
    url(r'^', include('wheatgrass_blog.urls')),

    # Add the admin page because some templates require it
    url(r'^admin/', admin.site.urls),
]
