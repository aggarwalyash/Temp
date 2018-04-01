from django.conf.urls import url
from django.contrib import admin

# from myapis.views import UserCreateAPIView,UserLoginAPIView,UsersAPIView
from myapis.views import *

urlpatterns = [
    url(r'^login/$', UserLoginAPIView.as_view(), name='login'),
    url(r'^register/$', UserCreateAPIView.as_view(), name='register'),
    url(r'^users/all$', UsersAPIView.as_view(), name='users'),
    url(r'^profile/$', ProfileCreateAPIView.as_view(), name='profile'),
]
