from django.conf.urls import url
from django.conf.urls import include, url
from . import views


urlpatterns = [
    url(r'^login/$',  views.Login),
    url(r'^logout/$',  views.Logout),
    url(r'^register/$',  views.Register),
    url(r'^$',  views.Home),
    url(r'^gridview/$',  views.Grid),
    url(r'^result/$',  views.Result),
    url(r'^help/$',  views.Help),
]


