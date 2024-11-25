from django.urls import path 
from .views import SignUpView, edit_bio
urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("edit_bio/", edit_bio, name="edit_bio"),
]