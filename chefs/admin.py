
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm 
from .models import CustomUser

class CustomUserAdmin(UserAdmin): 
    add_form = CustomUserCreationForm 
    form = CustomUserChangeForm 
    model = CustomUser
    list_display = [
        "email",
        "username",
        "experience",
        "bio",
        "favoriteCuisine",
    ]
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("experience", "bio", "favoriteCuisine",)}),) 
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("experience", "bio", "favoriteCuisine",)}),)
admin.site.register(CustomUser, CustomUserAdmin)
