from django.contrib.auth.forms import UserCreationForm, UserChangeForm 
from .models import CustomUser
from django.forms import ModelForm

class CustomUserCreationForm(UserCreationForm): 
    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "experience", 
            "bio", 
            "favoriteCuisine",
        )

class CustomUserChangeForm(UserChangeForm): 
    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "experience", 
            "bio", 
            "favoriteCuisine",
        )

class EditBioForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['bio']