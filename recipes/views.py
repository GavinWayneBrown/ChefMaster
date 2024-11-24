from django.shortcuts import render, redirect, get_object_or_404
from .forms import (
    RecipeForm,
    InstructionForm,
    IngredientForm,
    InstructionFormSet,
    IngredientFormSet,
    CommentForm,
)
from django.forms import modelformset_factory
from django.views.generic import TemplateView
from .models import Recipe, Instruction, Ingredient, Category
from django.views import View
from django.contrib.auth.decorators import login_required
from hitcount.models import HitCount
from hitcount.views import HitCountMixin
import logging

logger = logging.getLogger(__name__)
from django.core.paginator import Paginator
from django.shortcuts import render


def home(request):
    recipe_list = Recipe.objects.all()  # Query your recipes
    paginator = Paginator(recipe_list, 6)  # 6 posts per page

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "test-home.html", {"page_obj": page_obj})


@login_required
def create_recipe(request):
    if request.method == "POST":
        recipe_form = RecipeForm(request.POST, request.FILES)
        instruction_formset = InstructionFormSet(
            request.POST, queryset=Instruction.objects.none()
        )
        ingredient_formset = IngredientFormSet(
            request.POST, queryset=Ingredient.objects.none()
        )

        if (
            recipe_form.is_valid()
            and instruction_formset.is_valid()
            and ingredient_formset.is_valid()
        ):
            recipe = recipe_form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            recipe_form.save_m2m()

            # Save instructions
            instructions = instruction_formset.save(commit=False)
            for i, instruction in enumerate(instructions):
                instruction.recipe = recipe
                instruction.order = i + 1
                instruction.save()

            # Save ingredients
            ingredients = ingredient_formset.save(commit=False)
            for ingredient in ingredients:
                ingredient.recipe = recipe
                ingredient.save()

            return redirect("recipe_detail", pk=recipe.pk)
    else:
        recipe_form = RecipeForm()
        instruction_formset = InstructionFormSet(queryset=Instruction.objects.none())
        ingredient_formset = IngredientFormSet(queryset=Ingredient.objects.none())

    return render(
        request,
        "recipe/create_recipe.html",
        {
            "recipe_form": recipe_form,
            "instruction_formset": instruction_formset,
            "ingredient_formset": ingredient_formset,
        },
    )


def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    instructions = Instruction.objects.filter(recipe=recipe).order_by("order")
    ingredients = Ingredient.objects.filter(recipe=recipe)
    comments = recipe.comments.all()

    # Hit count
    hit_count = HitCount.objects.get_for_object(recipe)
    HitCountMixin.hit_count(request, hit_count)

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("login")
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.recipe = recipe
            comment.author = request.user
            comment.save()
            return redirect("recipe_detail", pk=recipe.pk)
    else:
        comment_form = CommentForm()
    return render(
        request,
        "recipe/recipe_detail.html",
        {
            "recipe": recipe,
            "instructions": instructions,
            "ingredients": ingredients,
            "comments": comments,
            "comment_form": comment_form,
        },
    )
