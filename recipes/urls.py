from django.urls import path
from .views import HomePageView, create_recipe, recipe_detail

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("create/", create_recipe, name="create_recipe"),
    path('recipe/<int:pk>/', recipe_detail, name='recipe_detail'),
]
