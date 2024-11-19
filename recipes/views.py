from django.shortcuts import render, redirect, get_object_or_404
from .forms import RecipeForm, InstructionForm, IngredientForm, InstructionFormSet, IngredientFormSet
from django.forms import modelformset_factory
from django.views.generic import TemplateView
from .models import Recipe, Instruction, Ingredient
from django.views import View
from django.contrib.auth.decorators import login_required


class HomePageView(TemplateView):
    template_name = "test-home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recipe_list"] = Recipe.objects.all()
        return context


@login_required
def create_recipe(request):
    if request.method == "POST":
        recipe_form = RecipeForm(request.POST)
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
    instructions = Instruction.objects.filter(recipe=recipe).order_by('order')
    ingredients = Ingredient.objects.filter(recipe=recipe)

    return render(
        request, 
        'recipe/recipe_detail.html', 
        {
            'recipe': recipe, 
            'instructions': instructions, 
            'ingredients': ingredients
        }
    )
