from django.urls import path
from .views import HomePageView, create_recipe

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("create/", create_recipe, name="create_recipe"),
]
