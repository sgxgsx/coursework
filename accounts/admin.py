from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import MyUserCreationForm, MyUserChangeForm
from .models import MyUser


class MyUserAdmin(UserAdmin):
    model = MyUser
    add_form = MyUserCreationForm
    form = MyUserChangeForm


admin.site.register(MyUser, MyUserAdmin)
