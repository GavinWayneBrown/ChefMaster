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
            
        ]

    def __init__(self, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)
        for field in ['prep_time', 'cook_time', 'total_time']:
            if self.instance and getattr(self.instance, field):
                duration = getattr(self.instance, field)
                hours, remainder = divmod(duration.total_seconds(), 3600)
                minutes, _ = divmod(remainder, 60)
                self.fields[field].initial = f"{int(hours):02}:{int(minutes):02}"


class InstructionForm(forms.ModelForm):
    class Meta:
        model = Instruction
        fields = ["step"]


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ["item", "quantity", ]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields["text"].label = "Leave a comment for the chef!"
        self.fields["text"].required = False


# Inline formsets
# In forms.py
InstructionFormSet = inlineformset_factory(
    Recipe, Instruction, form=InstructionForm, extra=3, can_delete=False
)

IngredientFormSet = inlineformset_factory(
    Recipe, Ingredient, form=IngredientForm, extra=3, can_delete=False
)

InstructionFormSetEdit = inlineformset_factory(
    Recipe, Instruction, form=InstructionForm, extra=1, can_delete=True
)

IngredientFormSetEdit = inlineformset_factory(
    Recipe, Ingredient, form=IngredientForm, extra=1, can_delete=True
)