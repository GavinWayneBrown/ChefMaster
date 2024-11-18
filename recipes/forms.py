from django import forms
from .models import Recipe, Instruction, Ingredient
from django.forms import inlineformset_factory
from .fields import CustomDurationField


class RecipeForm(forms.ModelForm):
    prep_time = CustomDurationField(widget=forms.TextInput(attrs={'placeholder': 'HH:MM'}))
    cook_time = CustomDurationField(widget=forms.TextInput(attrs={'placeholder': 'HH:MM'}))
    total_time = CustomDurationField(widget=forms.TextInput(attrs={'placeholder': 'HH:MM'}))

    class Meta:
        model = Recipe
        fields = [
            "title",
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
