from django.urls import path
from .views import HomePageView, create_recipe, recipe_detail
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("create/", create_recipe, name="create_recipe"),
    path('recipe/<int:pk>/', recipe_detail, name='recipe_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)