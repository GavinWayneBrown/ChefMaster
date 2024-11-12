from django import forms
from .models import Recipe, Instruction, Ingredient
from django.forms import inlineformset_factory


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            "summary",
            "prep_time",
            "cook_time",
            "total_time",
            "servings",
        ]


class InstructionForm(forms.ModelForm):
    class Meta:
        model = Instruction
        fields = ["step"]


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ["item", "quantity"]


# Inline formsets
InstructionFormSet = inlineformset_factory(
    Recipe, Instruction, form=InstructionForm, extra=1
)
IngredientFormSet = inlineformset_factory(
    Recipe, Ingredient, form=IngredientForm, extra=1
)
