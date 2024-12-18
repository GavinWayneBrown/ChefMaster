from django.shortcuts import render, redirect, get_object_or_404
from .forms import (
    RecipeForm,
    InstructionForm,
    IngredientForm,
    InstructionFormSet,
    IngredientFormSet,
    InstructionFormSetEdit, 
    IngredientFormSetEdit,
    CommentForm,
)
from django.views.generic.edit import UpdateView, DeleteView
from .forms import RecipeForm, InstructionForm, IngredientForm
from django.urls import reverse_lazy
from django.forms import modelformset_factory
from django.views.generic import TemplateView
from .models import Recipe, Instruction, Ingredient, Category
from django.views import View
from django.contrib.auth.decorators import login_required
from hitcount.models import HitCount
from hitcount.views import HitCountMixin

from chefs.models import CustomUser

from django.core.paginator import Paginator
from django.shortcuts import render
from django.conf import settings


def home(request):
    query = request.GET.get('q')
    category_name = request.GET.get('category')
    min_views = request.GET.get('min_views')
    max_views = request.GET.get('max_views')
    min_rating = request.GET.get('min_rating')
    max_rating = request.GET.get('max_rating')
    sort_by = request.GET.get('sort_by')  # Example: "views" or "-rating"

    # Start with all recipes
    recipe_list = Recipe.objects.all()

    # Apply filters
    if query:
        recipe_list = recipe_list.filter(title__icontains=query)
    if category_name:
        recipe_list = recipe_list.filter(categories__name=category_name)
    if min_views:
        recipe_list = recipe_list.filter(hit_count_generic__hits__gte=min_views)
    if max_views:
        recipe_list = recipe_list.filter(hit_count_generic__hits__lte=max_views)
    if min_rating:
        recipe_list = recipe_list.filter(ratings__average__gte=min_rating)
    if max_rating:
        recipe_list = recipe_list.filter(ratings__average__lte=max_rating)
    
    # Apply sorting
    if sort_by:
        recipe_list = recipe_list.order_by(sort_by)

    # Pagination
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "test-home.html", {"page_obj": page_obj})

@login_required


class HomePageView(TemplateView):
    template_name = "test-home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recipe_list"] = Recipe.objects.all()
        return context

# views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.contrib.auth.decorators import login_required
from .models import Recipe, Instruction, Ingredient
from .forms import RecipeForm, InstructionFormSet, IngredientFormSet

class RecipeUpdateView(UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = "recipe_edit.html"
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['instruction_formset'] = InstructionFormSetEdit(self.request.POST, instance=self.object)
            data['ingredient_formset'] = IngredientFormSetEdit(self.request.POST, instance=self.object)
        else:
            data['instruction_formset'] = InstructionFormSetEdit(instance=self.object)
            data['ingredient_formset'] = IngredientFormSetEdit(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        instruction_formset = context['instruction_formset']
        ingredient_formset = context['ingredient_formset']
        if instruction_formset.is_valid() and ingredient_formset.is_valid():
            self.object = form.save()
            instruction_formset.instance = self.object
            ingredient_formset.instance = self.object
            instruction_formset.save()
            ingredient_formset.save()
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'files': self.request.FILES
            })
        return kwargs

class RecipeDeleteView(DeleteView): 
    model = Recipe
    template_name = "recipe_delete.html"
    success_url = reverse_lazy("home")


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

def recipes_by_author(request, author_id):
    author = get_object_or_404(CustomUser, pk=author_id)
    recipes = Recipe.objects.filter(author=author)  # Query your recipes
    paginator = Paginator(recipes, 9)  # 6 posts per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'recipe/recipe_by_author.html', {'author': author, "page_obj": page_obj})
