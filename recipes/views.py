from django.shortcuts import render, redirect
from .forms import RecipeForm, InstructionFormSet, IngredientFormSet
from django.views.generic import TemplateView

class HomePageView(TemplateView):
    template_name = "home.html"

def create_recipe(request):
    if request.method == "POST":
        recipe_form = RecipeForm(request.POST)
        instruction_formset = InstructionFormSet(request.POST)
        ingredient_formset = IngredientFormSet(request.POST)
        if (
            recipe_form.is_valid()
            and instruction_formset.is_valid()
            and ingredient_formset.is_valid()
        ):
            recipe = recipe_form.save()
            instructions = instruction_formset.save(commit=False)
            for instruction in instructions:
                instruction.recipe = recipe
                instruction.save()
            ingredients = ingredient_formset.save(commit=False)
            for ingredient in ingredients:
                ingredient.recipe = recipe
                ingredient.save()
            return redirect(
                "recipe_list"
            )  # Redirect to a list of recipes or another appropriate view
    else:
        recipe_form = RecipeForm()
        instruction_formset = InstructionFormSet()
        ingredient_formset = IngredientFormSet()

    return render(
        request,
        "create_recipe.html",
        {
            "recipe_form": recipe_form,
            "instruction_formset": instruction_formset,
            "ingredient_formset": ingredient_formset,
        },
    )
