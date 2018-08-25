from django.contrib.auth.base_user import BaseUserManager
#from django.contrib.auth.models import User
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

# Name my backend 'MyCustomBackend'
from FinLand import models
from FinLand.models import User

class Backend:
    # Create an authentication method
    # This is called by the standard Django login procedure
    def authenticate(self, user):
        return user

    # Required for your backend to work properly - unchanged in most scenarios
    def get_user(self, username):
        return User.get(username)


