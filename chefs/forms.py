from django.contrib.auth.forms import UserCreationForm, UserChangeForm 
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm): 
     class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ("experience", "bio", "favoriteCuisine",)

class CustomUserChangeForm(UserChangeForm): 
    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields