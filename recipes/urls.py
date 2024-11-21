from django.urls import path
from .views import home, create_recipe, recipe_detail
from django.conf import settings
from django.conf.urls.static import static
from .views import HomePageView, create_recipe, RecipeDetailView, RecipeDeleteView, RecipeUpdateView

urlpatterns = [
    path("", home, name="home"),
    path("create/", create_recipe, name="create_recipe"),
    path('recipe/<int:pk>/', RecipeDetailView.as_view(), name='recipe_detail'),
    path("<int:pk>/delete/", RecipeDeleteView.as_view(),name="recipe_delete"),
    path("<int:pk>/edit/", RecipeUpdateView.as_view(),name="recipe_edit"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)