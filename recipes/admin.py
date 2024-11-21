from django.contrib import admin
from .models import Recipe, Instruction, Ingredient, Category


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "summary",
        "prep_time",
        "cook_time",
        "total_time",
        "servings",
        "date",
    )
    search_fields = ("title", "summary")
    list_filter = ("categories", "date")
    filter_horizontal = ("categories",)  # For ManyToMany fields


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Instruction)
class InstructionAdmin(admin.ModelAdmin):
    list_display = ("step", "recipe")


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("item", "quantity", "recipe")
