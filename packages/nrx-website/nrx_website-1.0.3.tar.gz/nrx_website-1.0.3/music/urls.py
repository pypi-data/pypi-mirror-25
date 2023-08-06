
from django.conf.urls import url

from . import views

# name of the apps

app_name = 'music'
urlpatterns = [
    # /music
    url(r'^$',views.index,name='index'),
    # /music/<album_id>
    url(r'(?P<album_id>[0-9]+)/$',views.detail,name='detail'),

# /music/<album_id>/favourite
    url(r'(?P<album_id>[0-9]+)/favourite/$',views.favourite,name='favourite ')
]
