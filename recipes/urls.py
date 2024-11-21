from django.urls import path
from .views import HomePageView, create_recipe, RecipeDetailView, RecipeDeleteView, RecipeUpdateView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("create/", create_recipe, name="create_recipe"),
    path('recipe/<int:pk>/', RecipeDetailView.as_view(), name='recipe_detail'),
    path("<int:pk>/delete/", RecipeDeleteView.as_view(),name="recipe_delete"),
    path("<int:pk>/edit/", RecipeUpdateView.as_view(),name="recipe_edit"),
]
