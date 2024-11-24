from django import forms
from .models import Recipe, Instruction, Ingredient, Category, Comment
from django.forms import inlineformset_factory
from .fields import CustomDurationField


class RecipeForm(forms.ModelForm):
    prep_time = CustomDurationField(
        widget=forms.TextInput(attrs={"placeholder": "HH:MM"})
    )
    cook_time = CustomDurationField(
        widget=forms.TextInput(attrs={"placeholder": "HH:MM"})
    )
    total_time = CustomDurationField(
        widget=forms.TextInput(attrs={"placeholder": "HH:MM"})
    )
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Recipe
        fields = [
            "image",
            "title",
            "summary",
            "prep_time",
            "cook_time",
            "total_time",
            "servings",
            "categories",
        ]


class InstructionForm(forms.ModelForm):
    class Meta:
        model = Instruction
        fields = ["step"]


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ["item", "quantity"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]


# Inline formsets
# In forms.py
InstructionFormSet = inlineformset_factory(
    Recipe, Instruction, form=InstructionForm, extra=3, can_delete=False
)

IngredientFormSet = inlineformset_factory(
    Recipe, Ingredient, form=IngredientForm, extra=3, can_delete=False
)
