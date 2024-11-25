from django.urls import path
from .views import home, create_recipe, recipe_detail, recipes_by_author
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", home, name="home"),
    path("create/", create_recipe, name="create_recipe"),
    path('recipe/<int:pk>/', recipe_detail, name='recipe_detail'),
    path('author/<int:author_id>/', recipes_by_author, name='recipes_by_author'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
